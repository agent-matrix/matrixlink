import os

# --- Global timeouts (seconds)
DEFAULT_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "30"))

# --- Tenancy header (edge → services)
TENANT_HEADER = os.getenv("TENANT_HEADER", "X-Tenant-Id")

# --- Provider hint (optional). One of: ce|gcrun|apprunner|aca|knative|local
CLOUD_PROVIDER = os.getenv("CLOUD_PROVIDER", "").strip().lower()

# --- MCP Gateway (may be auto-resolved via providers)
MCP_BASE_URL  = os.getenv("MCP_BASE_URL", "").rstrip("/")
MCP_TOKEN     = os.getenv("MCP_BEARER_TOKEN", "")

# --- East–west bearer for agents
A2A_TOKEN     = os.getenv("A2A_SERVICE_TOKEN", "")

# --- Optional provider-generic service naming (auto-compute URLs if *_BASE_URL is empty)
# Common pattern: set SERVICE_NAME and DOMAIN_SUFFIX when you don’t want to hardcode full URLs.
# Examples:
#   MCP_SERVICE_NAME=mcp-gateway
#   ORCH_SERVICE_NAME=orchestrator
#   AGENTS_DOMAIN_PREFIX=agents            # used with DOMAIN_SUFFIX to form https://agents.<suffix>/<agent>/...
#   DOMAIN_SUFFIX=proj.region.codeengine.appdomain.cloud
MCP_SERVICE_NAME      = os.getenv("MCP_SERVICE_NAME", "mcp-gateway")
ORCH_SERVICE_NAME     = os.getenv("ORCH_SERVICE_NAME", "orchestrator")
AGENTS_DOMAIN_PREFIX  = os.getenv("AGENTS_DOMAIN_PREFIX", "agents")
DOMAIN_SUFFIX         = os.getenv("DOMAIN_SUFFIX", "").lstrip(".")  # e.g., proj.region.codeengine.appdomain.cloud

# Per-provider optional knobs
# For Cloud Run, App Runner, ACA, Knative you can pass full BASE_URLs or set DOMAIN_SUFFIX + SERVICE_NAME
# If custom domains are used, set the *_BASE_URL directly.
