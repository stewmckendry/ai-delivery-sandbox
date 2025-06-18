from __future__ import annotations

import asyncio
import uuid
from pathlib import Path
import logging

from app.storage import redis as redis_store
from app.storage import audit

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Time to keep challenge info in Redis (seconds)
TTL_SECONDS = 600


async def _await_response(challenge_id: str) -> str:
    """Poll Redis until a user response for ``challenge_id`` is available.

    Once a response is received, the temporary screenshot is removed from
    ``/tmp`` and the Redis key is cleaned up.
    """
    audit.log_event("system", "challenge_wait", {"id": challenge_id})
    while True:
        await asyncio.sleep(1)
        resp = redis_store.get_key(f"challenge:{challenge_id}:response")
        if resp:
            redis_store.delete_key(f"challenge:{challenge_id}:response")
            screenshot = redis_store.get_key(
                f"challenge:{challenge_id}:screenshot"
            )
            if screenshot:
                try:
                    Path(screenshot).unlink(missing_ok=True)
                except Exception as exc:  # noqa: BLE001
                    logger.error(
                        "[pause] Failed to delete screenshot %s: %s", screenshot, exc
                    )
            audit.log_event("system", "challenge_resume", {"id": challenge_id})
            return resp


async def prompt_user(page, description: str = "") -> str:
    """Pause scraping, capture screenshot and wait for user input."""
    challenge_id = str(uuid.uuid4())
    screenshot_path = f"/tmp/challenge_{challenge_id}.png"
    Path("/tmp").mkdir(exist_ok=True)
    await page.screenshot(path=screenshot_path)

    redis_store.set_key(
        f"challenge:{challenge_id}:status", "awaiting", expire=TTL_SECONDS
    )
    redis_store.set_key(
        f"challenge:{challenge_id}:screenshot", screenshot_path, expire=TTL_SECONDS
    )
    if description:
        redis_store.set_key(
            f"challenge:{challenge_id}:desc", description, expire=TTL_SECONDS
        )

    audit.log_event("system", "challenge_prompt", {"id": challenge_id})
    logger.info("[pause] Challenge %s saved %s", challenge_id, screenshot_path)
    return await _await_response(challenge_id)


async def detect_and_handle(page) -> bool:
    """Detect common login challenges and prompt the user for a response."""
    if await page.locator("input[name='otp']").is_visible():
        code = await prompt_user(page, "otp")
        await page.fill("input[name='otp']", code)
        await page.click("button[type='submit']")
        return True
    if await page.locator("img[alt*='captcha']").is_visible():
        text = await prompt_user(page, "captcha")
        await page.fill("input[name='captcha']", text)
        await page.click("button[type='submit']")
        return True
    if await page.locator("input[name='security_answer']").is_visible():
        answer = await prompt_user(page, "security_question")
        await page.fill("input[name='security_answer']", answer)
        await page.click("button[type='submit']")
        return True
    return False
