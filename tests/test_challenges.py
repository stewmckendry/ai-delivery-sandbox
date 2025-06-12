import asyncio
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.adapters.common import challenges


class FakeRedis:
    def __init__(self):
        self.store = {}

    def set_key(self, key, value, expire=None):
        self.store[key] = value
        return True

    def get_key(self, key):
        return self.store.get(key)

    def delete_key(self, key):
        return 1 if self.store.pop(key, None) is not None else 0


class DummyLocator:
    def __init__(self, visible):
        self._visible = visible

    async def is_visible(self):
        return self._visible


class DummyPage:
    def __init__(self):
        self.filled = {}
        self.clicked = []

    async def screenshot(self, path):
        Path(path).write_text("img")

    def locator(self, selector):
        if selector == "input[name='otp']":
            return DummyLocator(True)
        return DummyLocator(False)

    async def fill(self, selector, value):
        self.filled[selector] = value

    async def click(self, selector):
        self.clicked.append(selector)


def test_detect_and_handle(monkeypatch):
    store = {}
    fake = FakeRedis()
    monkeypatch.setattr(challenges, "redis_store", fake)
    events = []
    monkeypatch.setattr(challenges.audit, "log_event", lambda u, a, c: events.append(a))
    monkeypatch.setattr(challenges.uuid, "uuid4", lambda: "cid")

    page = DummyPage()

    async def send():
        await asyncio.sleep(0.05)
        fake.set_key("challenge:cid:response", "1111")

    async def run():
        waiter = asyncio.create_task(send())
        handled = await challenges.detect_and_handle(page)
        await waiter
        return handled

    result = asyncio.run(run())
    assert result is True
    assert page.filled["input[name='otp']"] == "1111"
    assert "challenge_prompt" in events
    assert fake.get_key("challenge:cid:screenshot")
