import asyncio
import sys
from pathlib import Path
from contextlib import asynccontextmanager

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.adapters.test_portal_b as test_portal_b


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


def test_scrape_test_portal_b(monkeypatch):
    monkeypatch.setattr(test_portal_b, "async_playwright", _dummy_playwright)
    result = asyncio.run(test_portal_b.scrape_test_portal_b())
    suffixes = sorted(Path(p).suffix for p in result["files"])
    assert suffixes == [".html", ".html", ".html", ".html", ".pdf", ".txt"]
    for p in result["files"]:
        assert Path(p).exists()
