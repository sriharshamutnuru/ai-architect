# -*- coding: utf-8 -*-
# Week 3 Day 2 — httpx: Client, base_url, timeouts, error handling

import httpx
import logging
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(message)s"
)
logger = logging.getLogger(__name__)

BASE = "https://httpbin.org"


# ── 1. httpx one-off call — same as requests.get() ───────
print("── 1. Basic httpx GET ──")
r = httpx.get(f"{BASE}/json", timeout=10)
r.raise_for_status()
data = r.json()
print(f"  Status:  {r.status_code}")
print(f"  Keys:    {list(data.keys())}")


# ── 2. httpx.Client with base_url ─────────────────────────
print("\n── 2. httpx.Client with base_url ──")
with httpx.Client(
    base_url=BASE,
    timeout=10.0,
    headers={
        "Authorization": "Bearer demo-key",
        "X-Client":      "bfsi-tools/1.0",
    }
) as client:
    r = client.get("/get", params={"circular": "RBI-101"})
    r.raise_for_status()
    data = r.json()
    print(f"  URL:    {data['url']}")
    print(f"  Params: {data['args']}")

    r2 = client.get("/headers")
    r2.raise_for_status()
    h = r2.json()["headers"]
    print(f"  X-Client on every call: {h.get('X-Client')}")


# ── 3. Typed timeout ──────────────────────────────────────
print("\n── 3. Timeout demo ──")
try:
    r = httpx.get(
        f"{BASE}/delay/3",   # server waits 3s
        timeout=1.5,         # we give it 1.5s
    )
except httpx.ReadTimeout:
    print("  ReadTimeout fired — as expected")
except httpx.ConnectTimeout:
    print("  ConnectTimeout — network issue")

# Fine-grained timeout object
timeout = httpx.Timeout(connect=5.0, read=30.0, write=5.0, pool=5.0)
r = httpx.get(f"{BASE}/get", timeout=timeout)
r.raise_for_status()
print(f"  Fine-grained timeout: status={r.status_code}")


# ── 4. Error handling per exception type ──────────────────
print("\n── 4. Error handling ──")

def safe_get(url: str, timeout: float = 10.0) -> dict | None:
    try:
        r = httpx.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP {e.response.status_code}: {e.response.url}")
    except httpx.ReadTimeout:
        logger.error(f"ReadTimeout: {url}")
    except httpx.ConnectError:
        logger.error(f"ConnectError: {url}")
    return None

cases = [
    (f"{BASE}/json",        10.0),
    (f"{BASE}/status/401",  10.0),
    (f"{BASE}/status/429",  10.0),
    (f"{BASE}/delay/3",      1.0),
]
for url, t in cases:
    result = safe_get(url, timeout=t)
    if result:
        print(f"  OK: {list(result.keys())}")


# ── 5. Context manager on your client ────────────────────
print("\n── 5. Context manager ──")

class SimpleClient:
    def __init__(self, base_url: str):
        self._client = httpx.Client(base_url=base_url, timeout=10.0)

    def get(self, path: str) -> dict | None:
        try:
            r = self._client.get(path)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP {e.response.status_code}")
            return None

    def __enter__(self): return self
    def __exit__(self, *args): self._client.close()

with SimpleClient(BASE) as c:
    data = c.get("/get")
    print(f"  Status via context manager: works ✓")


# ── 6. Full BFSIAPIClient — production-ready ──────────────
print("\n── 6. Full BFSIAPIClient ──")

@dataclass(frozen=True)
class ClientConfig:
    base_url:    str
    api_key:     str
    timeout:     float = 30.0
    max_retries: int   = 3


class BFSIAPIClient:
    def __init__(self, config: ClientConfig):
        self.config     = config
        self.call_count = 0
        self._errors:   list[str] = []
        self._client    = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type":  "application/json",
                "X-Client":      "bfsi-tools/1.0",
            }
        )
        logger.info(f"BFSIAPIClient ready — {config.base_url}")

    def get(self, path: str, params: dict = None) -> dict | None:
        self.call_count += 1
        try:
            r = self._client.get(path, params=params)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            msg = f"HTTP {e.response.status_code} on GET {path}"
            logger.error(msg)
            self._errors.append(msg)
        except httpx.TimeoutException:
            msg = f"Timeout on GET {path}"
            logger.error(msg)
            self._errors.append(msg)
        except httpx.ConnectError:
            msg = f"ConnectError on GET {path}"
            logger.error(msg)
            self._errors.append(msg)
        return None

    def post(self, path: str, payload: dict) -> dict | None:
        self.call_count += 1
        try:
            r = self._client.post(path, json=payload)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            msg = f"HTTP {e.response.status_code} on POST {path}"
            logger.error(msg)
            self._errors.append(msg)
        except httpx.TimeoutException:
            msg = f"Timeout on POST {path}"
            logger.error(msg)
            self._errors.append(msg)
        return None

    def stats(self) -> dict:
        return {
            "calls":        self.call_count,
            "errors":       len(self._errors),
            "success_rate": (
                f"{(self.call_count - len(self._errors)) / max(self.call_count, 1):.0%}"
            ),
        }

    def __enter__(self): return self
    def __exit__(self, *args): self._client.close()
    def __repr__(self) -> str:
        return (f"BFSIAPIClient("
                f"calls={self.call_count}, "
                f"errors={len(self._errors)})")


config = ClientConfig(
    base_url="https://httpbin.org",
    api_key="demo-key",
    timeout=10.0,
)

with BFSIAPIClient(config) as client:
    data = client.get("/get", params={"circular": "RBI-101"})
    if data:
        print(f"  GET params:  {data['args']}")

    result = client.post("/post", {"model": "claude-sonnet-4"})
    if result:
        print(f"  POST model:  {result['json']['model']}")

    # Trigger error paths
    client.get("/status/401")
    client.get("/status/429")

    print(f"\n  Stats: {client.stats()}")
    print(f"  {client}")