import inspect
import httpx
from starlette.testclient import TestClient as StarletteTestClient
from starlette.testclient import (
    _AsyncBackend,
    _TestClientTransport,
    _is_asgi3,
    _WrapASGI2,
)

# Starlette < 0.28 expects httpx.Client to accept 'app' argument. Patch if needed.
if "app" not in inspect.signature(httpx.Client.__init__).parameters:

    def _patched_init(
        self,
        app,
        base_url: str = "http://testserver",
        raise_server_exceptions: bool = True,
        root_path: str = "",
        backend: str = "asyncio",
        backend_options=None,
        cookies=None,
        headers=None,
    ) -> None:
        self.async_backend = _AsyncBackend(
            backend=backend, backend_options=backend_options or {}
        )
        if _is_asgi3(app):
            asgi_app = app
        else:
            asgi_app = _WrapASGI2(app)  # type: ignore[arg-type]
        self.app = asgi_app
        self.app_state = {}
        params = inspect.signature(_TestClientTransport.__init__).parameters
        kwargs = {
            "portal_factory": self._portal_factory,
            "raise_server_exceptions": raise_server_exceptions,
            "root_path": root_path,
            "app_state": self.app_state,
        }
        if "client" in params:
            kwargs["client"] = ("testserver", 80)
        transport = _TestClientTransport(self.app, **kwargs)
        if headers is None:
            headers = {}
        headers.setdefault("user-agent", "testclient")
        httpx.Client.__init__(
            self,
            base_url=base_url,
            headers=headers,
            transport=transport,
            follow_redirects=True,
            cookies=cookies,
        )

    StarletteTestClient.__init__ = _patched_init
