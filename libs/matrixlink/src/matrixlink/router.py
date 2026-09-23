"""Outcome-learning capability router.

The router owns no authority. It only converts verified historical signals into
routing preferences; Matrix OS/Guardian still decide whether delegation may occur.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable

from .network import AgentCandidate, EvidenceSignal, ReputationProfile, rank_candidates, update_reputation


@dataclass
class EvidenceRouter:
    profiles: Dict[tuple[str, str], ReputationProfile] = field(default_factory=dict)

    def observe(self, agent_id: str, signal: EvidenceSignal) -> ReputationProfile:
        key = (agent_id, signal.capability)
        current = self.profiles.get(key) or ReputationProfile(agent_id=agent_id, capability=signal.capability)
        updated = update_reputation(current, signal)
        self.profiles[key] = updated
        return updated

    def rank(self, candidates: Iterable[AgentCandidate], capability: str) -> list[AgentCandidate]:
        enriched = []
        for candidate in candidates:
            key = (candidate.offer.agent_id, capability)
            profile = self.profiles.get(key, candidate.reputation)
            enriched.append(AgentCandidate(
                offer=candidate.offer,
                reputation=profile,
                healthy=candidate.healthy,
                policy_compatible=candidate.policy_compatible,
            ))
        return rank_candidates(enriched, capability)
