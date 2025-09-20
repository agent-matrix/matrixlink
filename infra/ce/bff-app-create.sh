#!/usr/bin/env bash
set -euo pipefail

REG="${REGISTRY}/${NAMESPACE}"
TAG="${IMAGE_TAG}"

ibmcloud ce app create --name bff \
  --image "${REG}/bff:${TAG}" \
  --cpu 0.5 --memory 512Mi \
  --min-scale 1 --max-scale 15 \
  --port 8080 \
  --env MCP_BASE_URL="https://mcp-gateway.<project>.<region>.codeengine.appdomain.cloud" \
  --env MCP_BEARER_TOKEN=@secret:mcp-token \
  --env ADMIN_BEARER=@secret:admin-bearer \
  --env DATABASE_URL="sqlite:///./data.db"
