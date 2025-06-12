from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Dict

from playwright.async_api import async_playwright


async def scrape_portal_b(username: str, password: str, portal_url: str) -> List[Dict[str, str]]:
    """Log into Portal B and download up to three PDFs.

    Parameters
    ----------
    username: str
        Login username used for the portal.
    password: str
        Associated password.
    portal_url: str
        URL of the login page for Portal B.

    Returns
    -------
    List[Dict[str, str]]
        Metadata for saved files including ``file_path`` and ``source_url``.
    """

    saved_files: List[Dict[str, str]] = []
    tmp_dir = Path("/tmp")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(portal_url)

        await page.fill("#username", username)
        await page.fill("#password", password)
        await page.click("button.login-btn")
        await page.wait_for_load_state("networkidle")

        # Save post-login HTML
        dashboard_html = tmp_dir / "portal_b_dashboard.html"
        content = await page.content()
        dashboard_html.write_text(content, encoding="utf-8")
        saved_files.append({
            "file_path": str(dashboard_html),
            "source_url": str(page.url)
        })

        # Attempt to download up to three PDF links on the page
        pdf_links = page.locator("a[href$='.pdf']")
        count = await pdf_links.count()
        for i in range(min(count, 3)):
            link = pdf_links.nth(i)
            href = await link.get_attribute("href")
            if not href:
                continue
            async with page.expect_download() as download_info:
                await link.click()
            download = await download_info.value
            file_name = download.suggested_filename
            save_path = tmp_dir / file_name
            await download.save_as(save_path)
            saved_files.append({
                "file_path": str(save_path),
                "source_url": href,
            })

        await browser.close()

    return saved_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape Portal B for documents.")
    parser.add_argument("--username", required=True, help="Portal username")
    parser.add_argument("--password", required=True, help="Portal password")
    parser.add_argument("--url", required=True, help="Login page URL")
    args = parser.parse_args()

    results = asyncio.run(scrape_portal_b(args.username, args.password, args.url))
    for item in results:
        print(item)

