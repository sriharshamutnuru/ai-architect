# -*- coding: utf-8 -*-
# Week 3 Day 1 — HTTP, GET, POST, headers, params, Session

import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(message)s"
)
logger = logging.getLogger(__name__)

BASE = "https://httpbin.org"


# ── 1. Status code classifier ─────────────────────────────
def classify_status(code: int) -> str:
    if code < 300:   return f"{code}: Success"
    elif code == 401: return f"{code}: Bad API key — check .env"
    elif code == 429: return f"{code}: Rate limited — wait and retry"
    elif code < 500:  return f"{code}: Client error — fix your request"
    else:             return f"{code}: Server error — retry later"

print("── Status codes ──")
for c in [200, 201, 401, 429, 404, 500]:
    print(f"  {classify_status(c)}")


# ── 2. Basic GET + raise_for_status ──────────────────────
print("\n── Basic GET ──")
try:
    r = requests.get(f"{BASE}/json", timeout=10)
    r.raise_for_status()
    data = r.json()
    logger.info(f"Status: {r.status_code}")
    logger.info(f"Content-Type: {r.headers.get('Content-Type')}")
    print(f"  Response keys: {list(data.keys())}")
except requests.HTTPError as e:
    logger.error(f"HTTP error: {e}")
except requests.ConnectionError:
    logger.error("Connection failed")
except requests.Timeout:
    logger.error("Request timed out")


# ── 3. GET with query parameters ─────────────────────────
print("\n── GET with params ──")
r = requests.get(
    f"{BASE}/get",
    params={"circular": "RBI-101", "tier": "high", "limit": 10},
    timeout=10,
)
r.raise_for_status()
data = r.json()
print(f"  URL:    {data['url']}")
print(f"  Params: {data['args']}")


# ── 4. GET with headers ───────────────────────────────────
print("\n── GET with headers ──")
r = requests.get(
    f"{BASE}/headers",
    headers={
        "Authorization": "Bearer demo-key",
        "X-Client":      "bfsi-tools/1.0",
        "Accept":        "application/json",
    },
    timeout=10,
)
r.raise_for_status()
sent = r.json()["headers"]
print(f"  Authorization: {sent.get('Authorization')}")
print(f"  X-Client:      {sent.get('X-Client')}")


# ── 5. POST with JSON body ────────────────────────────────
print("\n── POST with JSON body ──")
payload = {
    "model":      "claude-sonnet-4",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Summarise RBI KYC circular"}
    ]
}
r = requests.post(
    f"{BASE}/post",
    json=payload,
    headers={"Authorization": "Bearer demo-key"},
    timeout=10,
)
r.raise_for_status()
echo = r.json()["json"]
print(f"  Model sent:  {echo['model']}")
print(f"  Max tokens:  {echo['max_tokens']}")
print(f"  Message:     {echo['messages'][0]['content']}")


# ── 6. Session — shared headers ───────────────────────────
print("\n── Session ──")
with requests.Session() as session:
    session.headers.update({
        "Authorization": "Bearer demo-key",
        "X-Client":      "bfsi-tools/1.0",
        "Content-Type":  "application/json",
    })

    for path in ["/get", "/headers"]:
        r = session.get(f"{BASE}{path}", timeout=10)
        r.raise_for_status()
        print(f"  {path}: {r.status_code}")

    # Confirm headers were sent on all calls
    r = session.get(f"{BASE}/headers", timeout=10)
    h = r.json()["headers"]
    print(f"  X-Client on all calls: {h.get('X-Client')}")


# ── 7. BFSIAPIClient with real Session ────────────────────
print("\n── BFSIAPIClient ──")

class BFSIAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url   = base_url
        self.call_count = 0
        self._session   = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type":  "application/json",
            "X-Client":      "bfsi-tools/1.0",
        })
        logger.info(f"BFSIAPIClient ready — {base_url}")

    def get(self, path: str, params: dict = None) -> dict:
        self.call_count += 1
        url = f"{self.base_url}{path}"
        r = self._session.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, payload: dict) -> dict:
        self.call_count += 1
        url = f"{self.base_url}{path}"
        r = self._session.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()

    def __repr__(self) -> str:
        return (f"BFSIAPIClient(url='{self.base_url}', "
                f"calls={self.call_count})")


client = BFSIAPIClient("https://httpbin.org", "demo-key")

data = client.get("/get", params={"circular": "RBI-101"})
print(f"  GET params: {data['args']}")

result = client.post("/post", {"model": "claude-sonnet-4"})
print(f"  POST echo:  {result['json']['model']}")

print(f"  {client}")