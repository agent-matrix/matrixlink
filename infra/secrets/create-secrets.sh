#!/usr/bin/env bash
set -euo pipefail

# One-time per CE project. Rotate on schedule.
# Replace placeholders with real token strings or use --from-file if preferred.
ibmcloud ce secret create --name mcp-token     --from-literal token=<PASTE_MCP_GATEWAY_SERVICE_JWT>
ibmcloud ce secret create --name admin-bearer  --from-literal token=<PASTE_BFF_ADMIN_BEARER>
ibmcloud ce secret create --name a2a-token     --from-literal token=<PASTE_EAST_WEST_SERVICE_TOKEN>
