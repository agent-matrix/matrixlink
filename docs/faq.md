# FAQ

**Do I need MCP Gateway to start?**
No. You can run BFF + UI locally without MCP. Add MCP when you need discovery, health-based routing, and policy/RBAC.

**How does MatrixLink find URLs?**
Either via explicit `*_BASE_URL` envs, or by composing `https://<SERVICE>.<DOMAIN_SUFFIX>` using provider hints.

**Can I run agents/orchestrators at scale-to-zero?**
Yes. Keep MCP and BFF warm (`minScale=1`) and let agents/orchestrators scale to 0/∞.

**What about multi-cloud?**
MatrixLink is provider-agnostic. Move workloads between CE/Run/App Runner/ACA/Knative with env changes only.
