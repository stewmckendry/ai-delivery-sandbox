import asyncio
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# ensure repo root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.adapters.test_portal as test_portal


@asynccontextmanager
async def _dummy_playwright():
    class DummyPage:
        async def goto(self, url):
            pass

        async def fill(self, selector, value):
            pass

        async def click(self, selector):
            pass

        async def wait_for_load_state(self, state):
            pass

    class DummyBrowser:
        async def new_page(self):
            return DummyPage()

        async def close(self):
            pass

    class DummyChromium:
        async def launch(self, headless=True):
            return DummyBrowser()

    class DummyCtx:
        def __init__(self):
            self.chromium = DummyChromium()

    yield DummyCtx()


def test_scrape_test_portal(monkeypatch):
    monkeypatch.setattr(test_portal, "async_playwright", _dummy_playwright)
    result = asyncio.run(test_portal.scrape_test_portal())
    assert sorted(Path(p).suffix for p in result["files"]) == [".html", ".html", ".pdf"]
    for p in result["files"]:
        assert Path(p).exists()
