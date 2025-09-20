from __future__ import annotations
import time
import random
from typing import Dict, Optional

def backoff_gen(base: float = 0.2, cap: float = 3.0):
    """Exponential backoff with jitter."""
    attempt = 0
    while True:
        sleep = min(cap, base * (2 ** attempt)) * (0.5 + random.random() / 2)
        yield sleep
        attempt += 1

def auth_header(bearer: Optional[str]) -> Dict[str, str]:
    h: Dict[str, str] = {}
    if bearer:
        h["authorization"] = f"Bearer {bearer}"
    return h
