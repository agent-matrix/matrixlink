#!/usr/bin/env bash
set -euo pipefail

# Generic agent deploy; set NAME and IMAGE externally or via env
: "${NAME:?NAME required, e.g. NAME=a2a-candidate-ranker}"
: "${IMAGE:?IMAGE required, e.g. IMAGE=us.icr.io/ns/a2a-candidate-ranker:latest}"

ibmcloud ce app create --name "${NAME}" \
  --image "${IMAGE}" \
  --port 8080 \
  --min-scale 0 --max-scale 30 \
  --cpu 0.5 --memory 1Gi \
  --env REQUIRE_BEARER_TOKEN=@secret:a2a-token
