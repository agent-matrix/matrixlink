import os
import httpx
from fastapi import HTTPException
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# Try to resolve MCP base URL; prefer env, then matrixlink (if available), else local default.
def _resolve_mcp_base_url() -> str:
    # 1) Explicit env wins
    env_base = os.getenv("MCP_BASE_URL", "").strip().rstrip("/")
    if env_base:
        return env_base

    # 2) Use matrixlink.providers if installed
    try:
        from matrixlink.providers import resolve_mcp_base_url  # type: ignore
        val = (resolve_mcp_base_url() or "").strip().rstrip("/")
        if val:
            return val
    except Exception:
        pass

    # 3) Sensible local fallback
    cloud = (os.getenv("CLOUD_PROVIDER", "local") or "local").strip().lower()
    if cloud in ("local", "dev", ""):
        # Default local MCP Gateway
        return "http://localhost:4444"

    # 4) Last-resort: empty (will 500 at call-time with a clear message)
    return ""

MCP_BASE = _resolve_mcp_base_url()
MCP_TOKEN = os.getenv("MCP_BEARER_TOKEN", "").strip()

def _hdr():
    return {"Authorization": f"Bearer {MCP_TOKEN}"} if MCP_TOKEN else {}

def _url(p: str) -> str:
    base = MCP_BASE.rstrip("/")
    if not base:
        raise HTTPException(
            500,
            "MCP base URL not available. Set MCP_BASE_URL or provide provider hints "
            "(DOMAIN_SUFFIX + MCP_SERVICE_NAME), or ensure local default is reachable.",
        )
    return f"{base}{p}"

@retry(wait=wait_exponential(min=0.3, max=3), stop=stop_after_attempt(3), retry=retry_if_exception_type(httpx.HTTPError))
def list_servers():
    with httpx.Client(timeout=20) as c:
        r = c.get(_url("/admin/servers"), headers=_hdr())
        r.raise_for_status()
        return r.json()

@retry(wait=wait_exponential(min=0.3, max=3), stop=stop_after_attempt(3), retry=retry_if_exception_type(httpx.HTTPError))
def list_tools():
    with httpx.Client(timeout=20) as c:
        r = c.get(_url("/admin/tools"), headers=_hdr())
        r.raise_for_status()
        return r.json()

@retry(wait=wait_exponential(min=0.3, max=3), stop=stop_after_attempt(3), retry=retry_if_exception_type(httpx.HTTPError))
def create_server(payload: dict):
    with httpx.Client(timeout=30) as c:
        r = c.post(_url("/admin/servers"), headers=_hdr(), json=payload)
        r.raise_for_status()
        return r.json()

@retry(wait=wait_exponential(min=0.3, max=3), stop=stop_after_attempt(3), retry=retry_if_exception_type(httpx.HTTPError))
def assert_server(server_id: str) -> str:
    with httpx.Client(timeout=20) as c:
        r = c.get(_url(f"/admin/servers/{server_id}"), headers=_hdr())
        if r.status_code >= 400:
            raise HTTPException(404, "MCP server not found")
    return f"{MCP_BASE}/servers/{server_id}"

@retry(wait=wait_exponential(min=0.3, max=3), stop=stop_after_attempt(3), retry=retry_if_exception_type(httpx.HTTPError))
def health():
    try:
        with httpx.Client(timeout=10) as c:
            r = c.get(_url("/health"), headers=_hdr())
            r.raise_for_status()
            return {"ok": True}
    except Exception:
        return {"ok": False}
