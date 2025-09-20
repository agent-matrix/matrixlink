#!/usr/bin/env bash
set -euo pipefail

# Example for an external orchestrator service (separate repo/image)
# Edit IMAGE reference and envs for your orchestrator.
: "${IMAGE:?IMAGE required, e.g. IMAGE=us.icr.io/ns/orchestrator:latest}"

ibmcloud ce app create --name orchestrator \
  --image "${IMAGE}" \
  --port 8080 \
  --min-scale 0 --max-scale 20 \
  --cpu 0.5 --memory 1Gi \
  --env MCP_GATEWAY_URL="https://mcp-gateway.<project>.<region>.codeengine.appdomain.cloud" \
  --env MCP_DISCOVERY_TOKEN=@secret:mcp-token \
  --env A2A_SERVICE_TOKEN=@secret:a2a-token \
  --env TENANT_HEADER="X-Tenant-Id"
