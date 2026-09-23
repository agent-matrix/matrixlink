from matrixlink.network import (
    AgentCandidate,
    CapabilityOffer,
    DelegationRequest,
    EvidenceSignal,
    ReputationProfile,
    delegation_payload,
    rank_candidates,
    update_reputation,
)
from matrixlink.router import EvidenceRouter


def test_unverified_signal_does_not_change_reputation():
    p = ReputationProfile("a", "code.repair")
    s = EvidenceSignal("r1", "code.repair", False, True, 1.0)
    assert update_reputation(p, s) == p


def test_safety_failure_hurts_ranking():
    good = ReputationProfile("good", "code.repair", 10, 9, .9, 0, .8, .8)
    bad = ReputationProfile("bad", "code.repair", 10, 10, 1.0, 2, 1, 1)
    offer1 = CapabilityOffer("good", "code.repair", "http://good")
    offer2 = CapabilityOffer("bad", "code.repair", "http://bad")
    ranked = rank_candidates([AgentCandidate(offer2, bad), AgentCandidate(offer1, good)], "code.repair")
    assert ranked[0].offer.agent_id == "good"


def test_delegation_requires_proof():
    req = DelegationRequest("run", "trace", "s1", "code.repair", "fix it", (), ("pytest",))
    try:
        delegation_payload(req)
    except ValueError:
        pass
    else:
        raise AssertionError("delegation without success criteria must fail")


def test_router_learns_from_verified_outcomes():
    router = EvidenceRouter()
    router.observe("a", EvidenceSignal("r1", "research", True, True, .95))
    assert router.profiles[("a", "research")].verified_runs == 1
