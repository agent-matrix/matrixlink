import httpx, os
from fastapi import HTTPException
from matrixlink.providers import resolve_agents_base_url

AGENTS_BASE = (os.getenv("AGENTS_BASE_URL", "").rstrip("/") or (resolve_agents_base_url() or ""))
AGENTS_TOKEN = os.getenv("AGENTS_API_TOKEN", "")

def _hdr():
    h = {"Content-Type": "application/json"}
    if AGENTS_TOKEN:
        h["Authorization"] = f"Bearer {AGENTS_TOKEN}"
    return h

def agent_invoke_url(agent_name: str) -> str:
    base = AGENTS_BASE.rstrip("/")
    if not base:
        raise HTTPException(500, "AGENTS_BASE_URL not set and could not be auto-resolved (set DOMAIN_SUFFIX + AGENTS_DOMAIN_PREFIX or AGENTS_BASE_URL).")
    # Routing pattern: https://agents.<suffix>/<agent-name>/run
    return f"{base}/{agent_name}/run"

def call_agent_http(agent_url: str, payload: dict) -> dict:
    with httpx.Client(timeout=180) as c:
        r = c.post(agent_url, headers=_hdr(), json=payload)
        r.raise_for_status()
        return r.json()
