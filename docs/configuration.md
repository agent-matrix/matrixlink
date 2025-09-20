# Configuration

## Environment variables (BFF)
- `ADMIN_BEARER`
- `MCP_BASE_URL`
- `MCP_BEARER_TOKEN`
- `AGENTS_BASE_URL`
- `AGENTS_API_TOKEN`

## Environment variables (MatrixLink)
- `CLOUD_PROVIDER` — local|ce|gcrun|apprunner|aca|knative
- `DOMAIN_SUFFIX` — e.g. proj.region.codeengine.appdomain.cloud
- `MCP_SERVICE_NAME` — default mcp-gateway
- `ORCH_SERVICE_NAME` — default orchestrator
- `AGENTS_DOMAIN_PREFIX` — default agents
- `MCP_BASE_URL`, `ORCH_BASE_URL`, `AGENTS_BASE_URL`
- `MCP_BEARER_TOKEN`, `A2A_SERVICE_TOKEN`, `TENANT_HEADER`, `REQUEST_TIMEOUT`

## Provider presets
```bash
# Code Engine
CLOUD_PROVIDER=ce
DOMAIN_SUFFIX=proj.region.codeengine.appdomain.cloud
MCP_SERVICE_NAME=mcp-gateway
ORCH_SERVICE_NAME=orchestrator
AGENTS_DOMAIN_PREFIX=agents
```
