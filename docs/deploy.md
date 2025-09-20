# Deploy

## IBM Code Engine
1. Create secrets:
    ```bash
    ./infra/secrets/create-secrets.sh
    ```
2. Build & push images:
    ```bash
    make docker-build-bff docker-build-ui
    make docker-push-bff docker-push-ui
    ```
3. Create apps:
    ```bash
    make ce-create-bff
    make ce-create-ui
    ```
4. Configure API Gateway routes:
    * `/api/health|/api/ready|/api/admin/*|/api/mcp/*` -> BFF
    * `/api/chat` (or `/api/flows/<flow>`)               -> Orchestrator

## Other providers
Use env presets from **Configuration**. Endpoints resolve via either explicit `*_BASE_URL` or `DOMAIN_SUFFIX` + `SERVICE_NAME`.
