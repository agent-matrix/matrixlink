import httpx
from .config import MCP_TOKEN, DEFAULT_TIMEOUT
from .errors import MatrixLinkError
from .providers import resolve_mcp_base_url

class MCPClient:
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout: float = DEFAULT_TIMEOUT):
        self.base = (base_url or resolve_mcp_base_url() or "").rstrip("/")
        self.token = token or MCP_TOKEN
        self.timeout = timeout
        if not self.base:
            raise MatrixLinkError("MCP base URL not configured (set MCP_BASE_URL or DOMAIN_SUFFIX + MCP_SERVICE_NAME).")

    def _h(self):
        h = {"accept": "application/json"}
        if self.token:
            h["authorization"] = f"Bearer {self.token}"
        return h

    # -------- Discovery
    def discover_agents(self, *, skill: str, input_mode: str = "application/json", output_mode: str = "application/json", healthy_only: bool = True):
        with httpx.Client(timeout=self.timeout) as c:
            r = c.get(
                f"{self.base}/discover/agents",
                headers=self._h(),
                params={"skill": skill, "inputMode": input_mode, "outputMode": output_mode, "healthyOnly": str(healthy_only).lower()},
            )
            r.raise_for_status()
            return r.json() or []

    def discover_servers(self, *, role: str | None = None, tags: list[str] | None = None):
        with httpx.Client(timeout=self.timeout) as c:
            r = c.get(
                f"{self.base}/discover/servers",
                headers=self._h(),
                params={"role": role, "tags": ",".join(tags or [])},
            )
            r.raise_for_status()
            return r.json() or []

    # -------- Orchestrator helper (by tag or domain)
    def select_orchestrator(self, *, domain: str | None = None, tags: list[str] | None = None) -> dict | None:
        """
        Returns one orchestrator server record matching domain (tag) or tags. Strategy: pick first healthy.
        """
        qtags = list(tags or [])
        if domain:
            qtags.append(f"domain:{domain}")
        servers = self.discover_servers(role="orchestrator", tags=qtags)
        return servers[0] if servers else None
