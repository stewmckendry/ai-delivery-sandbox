"""
Prototype: Playwright + Redis + User Prompt for Login Challenges

This script simulates the orchestration loop for detecting login challenges (MFA, CAPTCHA), pausing,
and resuming after human input. Designed to work alongside a chat-based UX (e.g., ChatGPT MCP or CLI).
"""

import asyncio
import uuid
import time
from pathlib import Path

import redis.asyncio as redis
from playwright.async_api import async_playwright

redis_client = redis.Redis(decode_responses=True)
TTL = 600  # seconds

async def prompt_user(challenge_id: str, screenshot_path: str):
    print(f"[pause] Challenge encountered. Screenshot saved: {screenshot_path}")
    redis_client.set(f"challenge:{challenge_id}:status", "awaiting", ex=TTL)
    redis_client.set(f"challenge:{challenge_id}:screenshot", screenshot_path, ex=TTL)
    print(f"[pause] Waiting for user input via chat...")
    while True:
        time.sleep(3)
        response = redis_client.get(f"challenge:{challenge_id}:response")
        if response:
            print(f"[resume] Got user input: {response}")
            redis_client.delete(f"challenge:{challenge_id}:response")
            return response

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://example.com/login")

        await page.fill("#username", "test")
        await page.fill("#password", "123")
        await page.click("button[type='submit']")

        if await page.locator("text='Enter the code'").is_visible():
            challenge_id = str(uuid.uuid4())
            screenshot_path = f"tmp/challenge_{challenge_id}.png"
            Path("tmp").mkdir(exist_ok=True)
            await page.screenshot(path=screenshot_path)
            code = await prompt_user(challenge_id, screenshot_path)
            await page.fill("#otp", code)
            await page.click("button[type='submit']")

        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())