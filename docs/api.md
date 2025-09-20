# API

## Public endpoints (via BFF & Orchestrator)

| Method | Path | Description |
|---:|:---|---|
| GET | `/api/health` | Liveness |
| GET | `/api/ready` | Readiness (+ MCP health) |
| POST | `/api/chat` | Main chat entrypoint (edge → orchestrator) |

## Admin endpoints (BFF)

| Method | Path | Secured | Description |
|---:|:---|:---:|---|
| GET | `/api/mcp/servers` | ✅ | Proxy list MCP servers |
| GET | `/api/mcp/tools` | ✅ | Proxy list MCP tools |
| POST | `/api/mcp/servers` | ✅ | Create MCP server (proxy) |
| GET | `/api/admin/agents` | ✅ | List agents (local DB) |
| POST | `/api/admin/agents` | ✅ | Create agent |
| POST | `/api/admin/agents/{id}/bind` | ✅ | Bind agent → catalog URL |
| POST | `/api/admin/agents/{id}/run` | ✅ | Invoke agent by name |
