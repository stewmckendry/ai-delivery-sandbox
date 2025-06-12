"""Playwright test adapter that generates sample pages for pipeline QA."""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from playwright.async_api import async_playwright
import sys


async def scrape_test_portal(*_args, **_kwargs) -> Dict[str, List[str]]:
    """Generate mock portal pages and return saved file paths.

    The adapter creates a fake login page, a dashboard page linking to a PDF,
    and a visit summary page. It saves all content under ``/tmp`` with unique
    filenames so the orchestrator can parse them like real portal output.
    """

    load_dotenv()

    username = os.getenv("TEST_PORTAL_USERNAME") or os.getenv("MOCK_USERNAME") or "user"
    password = os.getenv("TEST_PORTAL_PASSWORD") or os.getenv("MOCK_PASSWORD") or "pass"

    tmp_dir = Path("/tmp")
    tmp_dir.mkdir(exist_ok=True)
    uid = uuid.uuid4().hex[:8]

    login_path = tmp_dir / f"test_login_{uid}.html"
    dash_path = tmp_dir / f"test_dash_{uid}.html"
    visit_path = tmp_dir / f"test_visit_{uid}.html"
    pdf_path = tmp_dir / f"test_labs_{uid}.pdf"

    login_html = f"""
    <html><body>
      <form id='login' action='{dash_path.name}' method='get'>
        <input id='username' name='username'>
        <input id='password' name='password' type='password'>
        <button id='login-btn' type='submit'>Login</button>
      </form>
    </body></html>
    """
    login_path.write_text(login_html, encoding="utf-8")

    dash_html = f"""
    <html><body>
      <a href='{pdf_path.name}'>Lab Results</a>
      <a href='{visit_path.name}'>Visit Summary</a>
    </body></html>
    """
    dash_path.write_text(dash_html, encoding="utf-8")

    # Reuse helper to create small sample files. Import dynamically so the
    # adapter works even when the repository root isn't on ``sys.path``.
    try:
        from scripts.e2e_test_runner import create_sample_pdf, create_sample_html
    except ModuleNotFoundError:  # pragma: no cover - fallback for packaged runs
        root = Path(__file__).resolve().parents[1]
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from scripts.e2e_test_runner import create_sample_pdf, create_sample_html

    create_sample_pdf(pdf_path)
    create_sample_html(visit_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(login_path.as_uri())
        await page.fill("#username", username)
        await page.fill("#password", password)
        await page.click("#login-btn")
        await page.wait_for_load_state("load")
        await browser.close()

    return {
        "files": [str(dash_path), str(visit_path), str(pdf_path)],
        "summary": {"pages": 2, "pdf_count": 1},
    }
