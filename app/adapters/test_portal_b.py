"""Playwright adapter that generates multi-page mock portal content."""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from playwright.async_api import async_playwright

from app.utils.sample_files import create_sample_pdf


async def scrape_test_portal_b(*_args, **_kwargs) -> Dict[str, List[str]]:
    """Generate a more complex mock portal with multiple pages.

    The adapter creates a fake login page that links to a dashboard with
    navigation to lab results, visit summaries and billing information.
    Visit summaries are shown inside a modal on the visits page, lab
    results are displayed in a table, and the billing page links to a
    downloadable summary text file. All files are stored under ``/tmp``
    with unique names so that repeated runs do not clash.
    """

    load_dotenv()

    username = os.getenv("TEST_PORTAL_USERNAME") or os.getenv("MOCK_USERNAME") or "user"
    password = os.getenv("TEST_PORTAL_PASSWORD") or os.getenv("MOCK_PASSWORD") or "pass"

    tmp_dir = Path("/tmp")
    tmp_dir.mkdir(exist_ok=True)
    uid = uuid.uuid4().hex[:8]

    login_path = tmp_dir / f"test_b_login_{uid}.html"
    dash_path = tmp_dir / f"test_b_dash_{uid}.html"
    visits_path = tmp_dir / f"test_b_visits_{uid}.html"
    labs_path = tmp_dir / f"test_b_labs_{uid}.html"
    billing_page_path = tmp_dir / f"test_b_billing_{uid}.html"
    billing_file_path = tmp_dir / f"billing_summary_{uid}.txt"

    # Login page with form redirecting to dashboard
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

    # Dashboard linking to other pages
    dash_html = f"""
    <html><body>
      <nav>
        <a href='{labs_path.name}'>Lab Results</a>
        <a href='{visits_path.name}'>Visits</a>
        <a href='{billing_page_path.name}'>Billing</a>
      </nav>
      <p>Welcome {username}</p>
    </body></html>
    """
    dash_path.write_text(dash_html, encoding="utf-8")

    # Visits page with modal visit summary
    visit_modal = """
    <div id='visit-modal' style='display:none'>
      <div class='visit'>
        <span class='date'>2023-06-01</span>
        <span class='provider'>General Hospital</span>
        <span class='doctor'>Dr. Jones</span>
        <p class='notes'>Routine check</p>
      </div>
    </div>
    """
    visits_html = f"""
    <html><body>
      <nav>
        <a href='{dash_path.name}'>Home</a>
        <a href='{labs_path.name}'>Labs</a>
        <a href='{billing_page_path.name}'>Billing</a>
      </nav>
      <button id='show-summary' onclick="document.getElementById('visit-modal').style.display='block'">View Visit Summary</button>
      {visit_modal}
    </body></html>
    """
    visits_path.write_text(visits_html, encoding="utf-8")

    # Labs page with table of results
    labs_html = f"""
    <html><body>
      <nav>
        <a href='{dash_path.name}'>Home</a>
        <a href='{visits_path.name}'>Visits</a>
        <a href='{billing_page_path.name}'>Billing</a>
      </nav>
      <table id='lab-table'>
        <tr><th>Test</th><th>Value</th><th>Date</th></tr>
        <tr><td>Cholesterol</td><td>5.8 mmol/L</td><td>2023-05-01</td></tr>
        <tr><td>Hemoglobin</td><td>13.5 g/dL</td><td>2023-05-02</td></tr>
      </table>
    </body></html>
    """
    labs_path.write_text(labs_html, encoding="utf-8")

    # Billing page linking to downloadable summary
    billing_file_path.write_text("Balance: $100\nDue: 2023-07-01", encoding="utf-8")
    billing_html = f"""
    <html><body>
      <nav>
        <a href='{dash_path.name}'>Home</a>
        <a href='{visits_path.name}'>Visits</a>
        <a href='{labs_path.name}'>Labs</a>
      </nav>
      <a href='{billing_file_path.name}' download>Download Billing Summary</a>
    </body></html>
    """
    billing_page_path.write_text(billing_html, encoding="utf-8")

    # Also create a PDF sample for variety
    pdf_path = tmp_dir / f"test_b_lab_{uid}.pdf"
    create_sample_pdf(pdf_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(login_path.as_uri())
        await page.fill("#username", username)
        await page.fill("#password", password)
        await page.click("#login-btn")
        await page.wait_for_load_state("load")
        await page.goto(visits_path.as_uri())
        await page.click("#show-summary")
        await page.goto(labs_path.as_uri())
        await page.goto(billing_page_path.as_uri())
        await browser.close()

    return {
        "files": [
            str(dash_path),
            str(visits_path),
            str(labs_path),
            str(billing_page_path),
            str(billing_file_path),
            str(pdf_path),
        ],
        "summary": {"pages": 4, "pdf_count": 1},
    }
