# Quickstart

## Prereqs
- Python 3.10+
- Node 18+
- Docker (optional)

## BFF (local)
```bash
make install
export ADMIN_BEARER=changeme-admin-bearer-token
export MCP_BASE_URL=http://localhost:4444  # optional if you run MCP locally
make run-bff
```
> Open: http://localhost:8080/api/health

## Admin UI (local)
```bash
make dev-ui
```
> Open: http://localhost:3000

## MatrixLink library
```bash
# dev install from repo
cd libs/matrixlink
pip install -e .

# or from PyPI once published
pip install matrixlink
```
