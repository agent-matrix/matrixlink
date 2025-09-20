# IBM Code Engine — Deploy Notes
## Public host (API Gateway):

- Route `/api/health|/api/ready|/api/admin/*|/api/mcp/*` -> BFF service
- Route `/api/chat` (or `/api/flows/<flow>`) -> Orchestrator service

All services bind `:8080` with unique hostnames.

## Edge policies:

- Verify OIDC/JWT for `/api/chat`
- Add/propagate `X-Request-Id` and optional `X-Tenant-Id`
- Rate limit, WAF, body size caps
- Do not buffer SSE (if streaming enabled)
