# Security & Ops

## Authentication & Authorization
- Edge: verify user OIDC/JWT for `/api/chat` and user-facing routes
- East–west: service bearer tokens; optionally mTLS between internal services
- Admin plane: `ADMIN_BEARER` for `/api/admin/*` and `/api/mcp/*`

## Tenancy & Headers
- Propagate `X-Tenant-Id` from edge → orchestrator → agents
- Enforce visibility in MCP (`private|team|global`) and team tags

## Observability
- Use `X-Request-Id` for correlation; structured logs
- Add OTEL exporters if desired; ensure SSE endpoints are not buffered by edge

## SLO Guidance
- Discovery P99 < 50 ms
- Agent success rate > 99.5% (ex-upstream)
- First SSE event < 250 ms

## Lifecycle & Rollouts
- Blue/green with tags (`canary`, `stable`)
- Traffic shaping in MCP; deprecate with policy windows

## Data & Secrets
- Store secrets in provider secret stores
- Never bake tokens into images; rotate regularly
