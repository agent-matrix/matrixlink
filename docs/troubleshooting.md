# Troubleshooting

**`ModuleNotFoundError: matrixlink` when running BFF locally**
- Run `make install` to install the library into the BFF venv.

**MCP base URL not set**
- Set `MCP_BASE_URL` or configure `CLOUD_PROVIDER` + `DOMAIN_SUFFIX` + `MCP_SERVICE_NAME`.

**CORS errors in the Admin UI**
- Set `CORS_ALLOW_ORIGINS` in BFF (e.g., `http://localhost:3000`).

**401 on admin routes**
- Set `ADMIN_BEARER` and pass `Authorization: Bearer <token>` from the UI Settings.

**SSE not streaming**
- Ensure your API Gateway does **not buffer** `text/event-stream` responses.
