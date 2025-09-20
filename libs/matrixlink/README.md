# MatrixLink
MatrixLink is a tiny, production-ready client for:

- MCP Gateway discovery (agents/servers) + admin (optional)
- A2A message send (HTTP+JSON)
- Orchestrator (MCP Server) invoke flows

## Configure (env or code)
- `MCP_BASE_URL`       — MCP Gateway base URL
- `MCP_BEARER_TOKEN`   — Bearer to call MCP
- `A2A_SERVICE_TOKEN`  — Bearer for east–west agent calls
- `TENANT_HEADER`      — header for tenancy (default `X-Tenant-Id`)
- `REQUEST_TIMEOUT`    — seconds (default 30)

## Quickstart
```python
from matrixlink import MCPClient, A2AClient, OrchestratorClient

mcp = MCPClient()
agents = mcp.discover_agents(skill="report.generate")

a2a = A2AClient()
resp = a2a.send_message(agents[0]["endpoint"], {"foo":"bar"})

orch = OrchestratorClient("[https://orchestrator.example](https://orchestrator.example)")
res  = orch.invoke("my.flow", {"arg":1})
```
