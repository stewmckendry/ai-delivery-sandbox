import os
import asyncio
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

PORTAL_URL = "https://mock-health-portal.dev/login"
DASHBOARD_PATH = Path("/tmp/portal_a_dashboard.html")
DOWNLOAD_DIR = Path("/tmp")


async def scrape_portal_a(username: str, password: str) -> dict:
    """Login to Portal A, save dashboard HTML and up to 3 PDF files."""
    saved_files: list[str] = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(PORTAL_URL)
        await page.fill("input[name='username']", username)
        await page.fill("input[name='password']", password)
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")

        content = await page.content()
        DASHBOARD_PATH.write_text(content, encoding="utf-8")
        saved_files.append(str(DASHBOARD_PATH))

        pdf_links = await page.eval_on_selector_all(
            "a[href$='.pdf']",
            "els => els.map(el => el.href)"
        )
        pdf_links = pdf_links[:3]

        for link in pdf_links:
            response = await context.request.get(link)
            if response.ok:
                filename = os.path.basename(urlparse(link).path) or "download.pdf"
                dest = DOWNLOAD_DIR / filename
                dest.write_bytes(await response.body())
                saved_files.append(str(dest))

        await browser.close()

    summary = {"pdf_count": len(saved_files) - 1}
    return {"files": saved_files, "summary": summary}


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Scrape Portal A")
    parser.add_argument("username", help="Portal username")
    parser.add_argument("password", help="Portal password")
    args = parser.parse_args()

    result = await scrape_portal_a(args.username, args.password)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
