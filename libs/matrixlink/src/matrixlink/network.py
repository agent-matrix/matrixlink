"""Governed A2A delegation and evidence-based reputation."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Tuple


@dataclass(frozen=True)
class EvidenceSignal:
    run_id: str
    capability: str
    verified: bool
    success: bool
    quality: float
    safety_violations: int = 0
    cost_score: float = 1.0
    latency_score: float = 1.0


@dataclass(frozen=True)
class ReputationProfile:
    agent_id: str
    capability: str
    verified_runs: int = 0
    successes: int = 0
    quality_ema: float = 0.5
    safety_violations: int = 0
    cost_ema: float = 0.5
    latency_ema: float = 0.5

    @property
    def reliability(self) -> float:
        if self.verified_runs == 0:
            return 0.0
        return self.successes / self.verified_runs

    @property
    def score(self) -> float:
        # Safety dominates; unverified/self-reported claims have no effect.
        base = (
            0.45 * self.reliability
            + 0.30 * self.quality_ema
            + 0.125 * self.cost_ema
            + 0.125 * self.latency_ema
        )
        penalty = min(1.0, 0.25 * self.safety_violations)
        confidence = min(1.0, self.verified_runs / 20.0)
        return max(0.0, (base - penalty) * (0.5 + 0.5 * confidence))


def update_reputation(profile: ReputationProfile, signal: EvidenceSignal, alpha: float = 0.2) -> ReputationProfile:
    if not signal.verified:
        return profile
    if signal.capability != profile.capability:
        return profile
    def ema(old: float, new: float) -> float:
        return (1 - alpha) * old + alpha * max(0.0, min(1.0, new))
    return replace(
        profile,
        verified_runs=profile.verified_runs + 1,
        successes=profile.successes + int(signal.success),
        quality_ema=ema(profile.quality_ema, signal.quality),
        safety_violations=profile.safety_violations + signal.safety_violations,
        cost_ema=ema(profile.cost_ema, signal.cost_score),
        latency_ema=ema(profile.latency_ema, signal.latency_score),
    )


@dataclass(frozen=True)
class CapabilityOffer:
    agent_id: str
    capability: str
    endpoint: str
    max_cost: float | None = None
    expected_latency_ms: int | None = None
    policy_tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class AgentCandidate:
    offer: CapabilityOffer
    reputation: ReputationProfile
    healthy: bool = True
    policy_compatible: bool = True


@dataclass(frozen=True)
class DelegationRequest:
    run_id: str
    trace_id: str
    parent_step_id: str
    capability: str
    objective: str
    success_criteria: Tuple[str, ...]
    verifiers: Tuple[str, ...]
    budget_limit: float | None = None
    policy_grant_id: str | None = None


def rank_candidates(candidates: Iterable[AgentCandidate], capability: str) -> list[AgentCandidate]:
    eligible = [
        c for c in candidates
        if c.healthy and c.policy_compatible
        and c.offer.capability == capability
        and c.reputation.capability == capability
    ]
    return sorted(eligible, key=lambda c: c.reputation.score, reverse=True)


def delegation_payload(request: DelegationRequest) -> dict:
    if not request.success_criteria or not request.verifiers:
        raise ValueError("delegation requires proof obligations")
    return {
        "run_id": request.run_id,
        "trace_id": request.trace_id,
        "parent_step_id": request.parent_step_id,
        "capability": request.capability,
        "objective": request.objective,
        "success_criteria": list(request.success_criteria),
        "verifiers": list(request.verifiers),
        "budget_limit": request.budget_limit,
        "policy_grant_id": request.policy_grant_id,
    }
