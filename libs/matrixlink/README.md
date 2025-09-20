# MatrixLink

[![PyPI Version](https://img.shields.io/pypi/v/matrixlink.svg)](https://pypi.org/project/matrixlink/)
[![Python Versions](https://img.shields.io/pypi/pyversions/matrixlink.svg)](https://pypi.org/project/matrixlink/)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
[![Docs](https://img.shields.io/badge/docs-matrixlink-blue?logo=mkdocs)](https://agent-matrix.github.io/matrixlink/)

**MatrixLink** is a compact, production-ready Python client for composing AI systems in the **MatrixHub** ecosystem:

* **MCP Gateway discovery** — find orchestrators and A2A agents by *skill*, *tags*, and *modes*, filtered by health/fitness.
* **A2A messaging** — call stateless agents via `POST /message/send` (optional SSE for streaming).
* **Orchestrator invoke** — call MCP Server flows via `POST /invoke/<flow>`.
* **Cloud-portable endpoints** — resolve service URLs from environment only (Local, **IBM Code Engine**, **Google Cloud Run**, **AWS App Runner**, **Azure Container Apps**, **Knative/Kubernetes**).

> Ship faster with safe vendor agility: **swap agents/orchestrators without changing app code**.

---

## Why MatrixLink (especially for consulting firms)

Consultancies need to deliver reliable AI workflows quickly, across many client environments, with minimal rework:

1. **One SDK, many runtimes**
   Same code works from local-dev to any major serverless/container platform. No provider-specific forks.

2. **Faster delivery**
   Discover proven agents/orchestrators from MatrixHub and wire them in minutes instead of rewriting capabilities.

3. **Governance-ready**
   Works with MCP Gateway for RBAC, visibility scoping, health & fitness signals, and controlled rollouts (canary/blue-green).

4. **Vendor flexibility**
   Keep multiple implementations for the same `skill` and select at runtime. Avoid hard binds to any one provider.

5. **Low-friction handoff**
   Ship portable solutions that customers can run in their preferred cloud with **env-only** changes.

---

## Installation

```bash
pip install matrixlink
# or
pipx install matrixlink
```

Requires **Python 3.10+**.

---

## Quickstart

```python
from matrixlink import MCPClient, A2AClient, OrchestratorClient

# 1) Discover agents by skill via MCP Gateway
mcp = MCPClient()  # reads MCP_BASE_URL or resolves with CLOUD_PROVIDER hints
agents = mcp.discover_agents(skill="report.generate")

# 2) Send a message to the best agent (A2A)
a2a = A2AClient()  # picks A2A_SERVICE_TOKEN from env if set
resp = a2a.send_message(agents[0]["endpoint"], {"title": "Weekly", "bullets": ["A", "B", "C"]})

# 3) Invoke an orchestrator flow (MCP server)
orch = OrchestratorClient("https://orchestrator.example.com")
result = orch.invoke("finance.generateReport", {"period": "Q3", "kpis": ["rev", "margin"]})
```

**No MCP?** You can still use `A2AClient` and `OrchestratorClient` directly with explicit URLs; add MCP later when you want discovery, health routing, and policy.

---

## API Overview

### MCPClient — discovery (via MCP Gateway)

```python
from matrixlink import MCPClient
mcp = MCPClient()

servers = mcp.discover_servers(role="orchestrator", tags=["domain:finance"])
agents  = mcp.discover_agents(
    skill="report.generate",
    input_mode="json",
    output_mode="json"
)
```

### A2AClient — agent messaging

```python
from matrixlink import A2AClient
client = A2AClient()  # uses A2A_SERVICE_TOKEN if set
result = client.send_message("https://agents.example.com/agent-synth", {"foo": "bar"})
```

### OrchestratorClient — flow invoke

```python
from matrixlink import OrchestratorClient
orch = OrchestratorClient("https://orchestrator.example.com")
reply = orch.invoke("finance.generateReport", {"period": "Q3"})
```

> Optional Server-Sent Events (SSE) helpers are included for streaming responses.

---

## Configuration (env first)

MatrixLink prefers **environment variables** (you can also pass kwargs).

**Core**

* `MCP_BASE_URL` — MCP Gateway base URL (e.g., `https://mcp.example.com`)
* `MCP_BEARER_TOKEN` — bearer token for MCP calls
* `A2A_SERVICE_TOKEN` — bearer token for agent (east–west) calls
* `TENANT_HEADER` — tenancy header name (default: `X-Tenant-Id`)
* `REQUEST_TIMEOUT` — HTTP timeout seconds (default: `30`)

**Provider hints (optional)**

* `CLOUD_PROVIDER` — `local` (default), `ce`, `gcrun`, `apprunner`, `aca`, `knative`
* `DOMAIN_SUFFIX` — e.g., `proj.region.codeengine.appdomain.cloud`
* `MCP_SERVICE_NAME` — default `mcp-gateway`
* `ORCH_SERVICE_NAME` — default `orchestrator`
* `AGENTS_DOMAIN_PREFIX` — default `agents`
* `ORCH_BASE_URL`, `AGENTS_BASE_URL` — explicit overrides

> If you set explicit `*_BASE_URL`, provider hints are ignored.


![](assets/matrixlink-usecase-vertical.svg)

---

## Supported cloud providers (and how resolution works)

MatrixLink resolves service endpoints from **env only**. You can:

* Set explicit URLs (`MCP_BASE_URL`, `ORCH_BASE_URL`, `AGENTS_BASE_URL`), **or**
* Provide provider hints and let MatrixLink compose URLs from service names + domain suffix.

| Provider                 | Minimal env example                                                                                           | Notes                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Local / Docker**       | `CLOUD_PROVIDER=local` + `MCP_BASE_URL=http://localhost:4444`                                                 | Ideal for dev/test.                                 |
| **IBM Code Engine**      | `CLOUD_PROVIDER=ce` + `DOMAIN_SUFFIX=proj.region.codeengine.appdomain.cloud` + `MCP_SERVICE_NAME=mcp-gateway` | Works with internal CE hostnames or custom domains. |
| **Google Cloud Run**     | `CLOUD_PROVIDER=gcrun` + explicit `MCP_BASE_URL/ORCH_BASE_URL/AGENTS_BASE_URL`                                | Prefer custom domains or Cloud Run URLs.            |
| **AWS App Runner**       | `CLOUD_PROVIDER=apprunner` + explicit `*_BASE_URL`                                                            | Use App Runner service URLs or custom domain.       |
| **Azure Container Apps** | `CLOUD_PROVIDER=aca` + `DOMAIN_SUFFIX=<env>.azurecontainerapps.io` + service names                            | Use ACA default domains or custom hostnames.        |
| **Knative / Kubernetes** | `CLOUD_PROVIDER=knative` + `DOMAIN_SUFFIX=apps.example.internal` + service names                              | Works with cluster DNS / service mesh.              |

This lets consulting teams **hand off** solutions to clients on their platform of choice with **no code changes**.

---

## Patterns consultants use with MatrixLink

* **Domain Orchestrator** — encode business logic in an MCP Server; discover skills at runtime; swap agent providers without redeploying callers.
* **BFF / Edge Facade** — keep a thin API layer; use `OrchestratorClient` inside to call flows; pass through tenancy and request IDs.
* **Multi-tenant apps** — enforce `X-Tenant-Id` throughout; leverage MCP visibility (`private|team|global`) to segment catalogs by client or BU.
* **Progressive hardening** — start with explicit URLs; add MCP Gateway for discovery, health, and fitness; introduce canary/blue-green via tags.
* **Hybrid & multi-cloud** — keep agents/orchestrators near data; choose endpoints per region/provider purely by env.

---

## Error handling

Exceptions live in `matrixlink.errors`:

* `DiscoveryError` — MCP discovery problems
* `AuthError` — missing/invalid tokens
* `HTTPError` — non-2xx responses
* `TimeoutError` — request timed out

```python
from matrixlink.errors import DiscoveryError, HTTPError
try:
    agent = MCPClient().discover_agents(skill="doc.classify")[0]
except DiscoveryError:
    # no agent found / MCP unreachable
    ...
```

---

## Security & operations

* Keep tokens in a **secret manager**; never bake into images.
* Propagate `X-Request-Id` and your `TENANT_HEADER` end-to-end for traceability.
* If using SSE, ensure your edge **does not buffer** `text/event-stream`.
* Keep MCP Gateway and your edge warm (min scale = 1) for low-latency discovery; let agents/orchestrators scale to zero.

---

## Versioning

Semantic versioning. Breaking changes bump **major**.

---

## Links

* **Docs** — [https://agent-matrix.github.io/matrixlink/](https://agent-matrix.github.io/matrixlink/)
* **Source** — [https://github.com/agent-matrix/matrixlink](https://github.com/agent-matrix/matrixlink)
* **Issues** — [https://github.com/agent-matrix/matrixlink/issues](https://github.com/agent-matrix/matrixlink/issues)

---

## License

Apache 2.0.
