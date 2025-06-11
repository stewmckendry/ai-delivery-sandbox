import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright


async def login_and_save():
    """Log in to mock health portal and save dashboard HTML."""
    load_dotenv()
    username = os.getenv("MOCK_USERNAME")
    password = os.getenv("MOCK_PASSWORD")
    if not username or not password:
        raise EnvironmentError("MOCK_USERNAME and MOCK_PASSWORD must be set in .env")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://mock-health-portal.dev/login")
        await page.fill("input[name='username']", username)
        await page.fill("input[name='password']", password)
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")
        content = await page.content()
        with open("login_page.html", "w", encoding="utf-8") as f:
            f.write(content)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(login_and_save())
