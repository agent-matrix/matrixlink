# Governed A2A network

MatrixLink is the inter-agent network plane. It discovers and delegates; it does
not become a second global orchestrator.

## Delegation envelope

Every A2A delegation carries:

- Agent-Matrix `run_id` and `trace_id`,
- parent plan step,
- requested capability,
- objective,
- proof obligations,
- verifier names,
- budget limit,
- policy-grant reference.

This preserves governance across distributed agent teams.

## Reputation

Reputation is **evidence-based, not self-reported**.

Only verified execution outcomes update a profile. Signals include task success,
quality, safety violations, cost efficiency and latency. Unverified claims are
ignored.

New agents start with low confidence rather than a fabricated perfect score.

## Capability market

A capability offer advertises what an agent can provide, endpoint, policy tags,
expected latency and optional maximum cost. It does not grant permission.
Matrix OS/Guardian remain responsible for authorization and Treasury remains
responsible for budgets.

## Learned routing

The EvidenceRouter incrementally learns routing preferences from verified
outcomes. It cannot bypass health or policy compatibility filters.
