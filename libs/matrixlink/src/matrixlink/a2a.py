import httpx
from .config import A2A_TOKEN, TENANT_HEADER, DEFAULT_TIMEOUT
from .sse import sse_iter

class A2AClient:
    def __init__(self, service_token: str | None = None, timeout: float = DEFAULT_TIMEOUT):
        self.token = service_token or A2A_TOKEN
        self.timeout = timeout

    def _headers(self, tenant: str | None = None):
        h = {"content-type": "application/json"}
        if self.token:
            h["authorization"] = f"Bearer {self.token}"
        if tenant:
            h[TENANT_HEADER] = tenant
        return h

    def send_message(self, endpoint: str, data_part: dict, *, tenant: str | None = None) -> dict:
        msg = {"role": "user", "parts": [{"kind": "data", "data": data_part}]}
        with httpx.Client(timeout=self.timeout) as c:
            r = c.post(f"{endpoint.rstrip('/')}/message/send", headers=self._headers(tenant), json=msg)
            r.raise_for_status()
            return r.json()

    def send_text(self, endpoint: str, text: str, *, tenant: str | None = None) -> dict:
        msg = {"role": "user", "parts": [{"kind": "text", "text": text}]}
        with httpx.Client(timeout=self.timeout) as c:
            r = c.post(f"{endpoint.rstrip('/')}/message/send", headers=self._headers(tenant), json=msg)
            r.raise_for_status()
            return r.json()

    def stream(self, endpoint: str, task_id: str, *, tenant: str | None = None, timeout: float | None = None):
        h = {}
        if self.token:
            h["authorization"] = f"Bearer {self.token}"
        if tenant:
            h[TENANT_HEADER] = tenant
        url = f"{endpoint.rstrip('/')}/message/stream?taskId={task_id}"
        yield from sse_iter(url, headers=h, timeout=timeout or (self.timeout * 10))
