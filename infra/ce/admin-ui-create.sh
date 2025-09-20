#!/usr/bin/env bash
set -euo pipefail

REG="${REGISTRY}/${NAMESPACE}"
TAG="${IMAGE_TAG}"

ibmcloud ce app create --name matrixhub-admin \
  --image "${REG}/matrixhub-admin:${TAG}" \
  --cpu 0.25 --memory 256Mi \
  --min-scale 0 --max-scale 10 \
  --port 8080
