#!/usr/bin/env bash
set -euo pipefail

REG="${REGISTRY}/${NAMESPACE}"
TAG="${IMAGE_TAG}"

ibmcloud ce app update --name bff --image "${REG}/bff:${TAG}"
