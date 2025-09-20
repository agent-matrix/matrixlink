# MCP Gateway — when and how to use it

**When you need it**
- Runtime discovery by skill/tags across many agents
- A registry with visibility, RBAC, health and fitness scoring
- Traffic shaping via tags (canary, tier) and safe rollouts

**Local dev**
- Run a lightweight MCP instance at `http://localhost:4444`
- Point BFF/clients with `MCP_BASE_URL=http://localhost:4444`

**Cloud**
- Deploy/consume a managed MCP; set `MCP_BASE_URL` (or use `DOMAIN_SUFFIX` + `MCP_SERVICE_NAME`)
- Use `MCP_BEARER_TOKEN` for service-to-service auth

**Discovery APIs (typical)**
- `GET /discover/agents?skill=...&inputMode=...&outputMode=...&healthyOnly=true`
- `GET /discover/servers?role=orchestrator&tags=...`

**Best practices**
- Keep MCP warm (`minScale=1`) for low latency discovery
- Enforce RBAC + tenancy headers end-to-end
- Emit heartbeats from agents/orchestrators with version & region tags
