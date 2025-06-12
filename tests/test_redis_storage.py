import importlib
import sys
import types
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class FakeRedis:
    def __init__(self, *args, **kwargs):
        self.store = {}

    def set(self, name, value, ex=None):
        self.store[name] = value
        return True

    def get(self, name):
        return self.store.get(name)

    def delete(self, name):
        return 1 if self.store.pop(name, None) is not None else 0

    def ping(self):
        return True


def test_set_get_delete(monkeypatch):
    fake_module = types.SimpleNamespace(Redis=FakeRedis, RedisError=Exception)
    monkeypatch.setitem(sys.modules, "redis", fake_module)
    monkeypatch.setitem(sys.modules, "dotenv", types.SimpleNamespace(load_dotenv=lambda: None))
    monkeypatch.setenv("REDIS_HOST", "localhost")
    monkeypatch.setenv("REDIS_PORT", "6379")
    monkeypatch.delenv("REDIS_PASSWORD", raising=False)
    module = importlib.import_module("app.storage.redis")
    importlib.reload(module)

    assert module.is_connected()

    module.set_key("foo", "bar")
    assert module.get_key("foo") == "bar"
    assert module.delete_key("foo") == 1
    assert module.get_key("foo") is None


