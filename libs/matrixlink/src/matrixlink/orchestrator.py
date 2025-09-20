import httpx
from .config import TENANT_HEADER, DEFAULT_TIMEOUT

class OrchestratorClient:
    def __init__(self, base_url: str, timeout: float = DEFAULT_TIMEOUT):
        self.base = base_url.rstrip("/")
        self.timeout = timeout

    def invoke(self, flow: str, arguments: dict, *, options: dict | None = None, tenant: str | None = None, bearer: str | None = None):
        h = {"content-type": "application/json"}
        if bearer:
            h["authorization"] = f"Bearer {bearer}"
        if tenant:
            h[TENANT_HEADER] = tenant
        payload = {"arguments": arguments or {}, "options": options or {}}
        with httpx.Client(timeout=self.timeout) as c:
            r = c.post(f"{self.base}/invoke/{flow}", headers=h, json=payload)
            r.raise_for_status()
            return r.json()
