from typing import Any

from httpx import AsyncClient


class AsyncApiTestClient(AsyncClient):
    _app = None
    auth_user = None

    def __init__(self, **kwargs):
        self._app = kwargs.get("app")
        super().__init__(**kwargs)

    def url_for(self, name: str, /, **path_params: Any) -> str:
        return self._app.url_path_for(name, **path_params)
