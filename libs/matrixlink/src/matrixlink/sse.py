from __future__ import annotations
import httpx
from typing import Iterator

def sse_iter(url: str, headers: dict | None = None, timeout: float = 300.0) -> Iterator[dict]:
    """
    Minimal SSE iterator: yields parsed 'event' frames as dicts with keys: event, data, id (if any).
    Assumes 'data' payload is JSON when possible; falls back to raw string.
    """
    headers = headers or {}
    headers.setdefault("accept", "text/event-stream")
    with httpx.Client(timeout=timeout) as c:
        with c.stream("GET", url, headers=headers) as r:
            r.raise_for_status()
            ev, data, eid = None, [], None
            for line in r.iter_lines():
                if not line:
                    if ev or data or eid:
                        payload = "\n".join(data)
                        try:
                            import json
                            parsed = json.loads(payload)
                        except Exception:
                            parsed = payload
                        yield {"event": ev or "message", "data": parsed, "id": eid}
                    ev, data, eid = None, [], None
                    continue
                if line.startswith("event:"):
                    ev = line.split(":", 1)[1].strip()
                elif line.startswith("id:"):
                    eid = line.split(":", 1)[1].strip()
                elif line.startswith("data:"):
                    data.append(line.split(":", 1)[1].lstrip())
