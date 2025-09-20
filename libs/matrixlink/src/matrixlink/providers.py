import os
from .config import (
    CLOUD_PROVIDER, DOMAIN_SUFFIX,
    MCP_BASE_URL, MCP_SERVICE_NAME,
    ORCH_SERVICE_NAME,
    AGENTS_DOMAIN_PREFIX,
)

def _mk_url(host: str, https: bool = True) -> str:
    scheme = "https" if https else "http"
    return f"{scheme}://{host}".rstrip("/")

def _maybe_custom(base_url_env: str) -> str | None:
    v = base_url_env.strip().rstrip("/") if base_url_env else ""
    return v or None

def resolve_mcp_base_url() -> str | None:
    # If explicitly provided, use it.
    if v := _maybe_custom(os.getenv("MCP_BASE_URL", MCP_BASE_URL)):
        return v

    if not DOMAIN_SUFFIX:
        # No domain suffix available; caller should error if still None.
        return None

    # Default scheme: https. All providers resolve to https hostnames.
    if CLOUD_PROVIDER in ("ce", "codeengine", ""):
        # IBM Code Engine: https://<service>.<domain_suffix>
        return _mk_url(f"{MCP_SERVICE_NAME}.{DOMAIN_SUFFIX}")

    if CLOUD_PROVIDER in ("gcrun", "cloudrun"):
        # Recommend setting MCP_BASE_URL directly for Cloud Run due to hashed hostnames.
        # If you mapped a custom domain to the service name on the same suffix, we try it:
        return _mk_url(f"{MCP_SERVICE_NAME}.{DOMAIN_SUFFIX}")

    if CLOUD_PROVIDER in ("apprunner", "aws-apprunner"):
        # App Runner typically uses random hostnames; prefer explicit MCP_BASE_URL.
        return _mk_url(f"{MCP_SERVICE_NAME}.{DOMAIN_SUFFIX}")

    if CLOUD_PROVIDER in ("aca", "azure", "azure-container-apps"):
        return _mk_url(f"{MCP_SERVICE_NAME}.{DOMAIN_SUFFIX}")

    if CLOUD_PROVIDER in ("knative", "k8s", "kubernetes"):
        return _mk_url(f"{MCP_SERVICE_NAME}.{DOMAIN_SUFFIX}")

    if CLOUD_PROVIDER in ("local", "dev"):
        # Compose/Local reverse proxy with a wildcard DNS (nip.io) or dev domain
        return _mk_url(f"{MCP_SERVICE_NAME}.{DOMAIN_SUFFIX or 'localhost'}", https=False)

    # Fallback
    return None

def resolve_orchestrator_base_url() -> str | None:
    # Prefer explicit env
    if v := _maybe_custom(os.getenv("ORCH_BASE_URL", "")):
        return v
    if not DOMAIN_SUFFIX:
        return None
    svc = os.getenv("ORCH_SERVICE_NAME", ORCH_SERVICE_NAME)
    return _mk_url(f"{svc}.{DOMAIN_SUFFIX}")

def resolve_agents_base_url() -> str | None:
    # Prefer explicit env
    if v := _maybe_custom(os.getenv("AGENTS_BASE_URL", "")):
        return v
    if not DOMAIN_SUFFIX:
        return None
    # Agents base is a path-style “fan-in” prefix host like https://agents.<suffix>
    # Actual agent endpoint becomes: <base>/<agent-name>/...
    prefix = os.getenv("AGENTS_DOMAIN_PREFIX", AGENTS_DOMAIN_PREFIX)
    return _mk_url(f"{prefix}.{DOMAIN_SUFFIX}")
