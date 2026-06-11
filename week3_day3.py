# -*- coding: utf-8 -*-
# Week 3 Day 3 — async/await, asyncio.gather(), httpx.AsyncClient

import asyncio
import httpx
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(message)s"
)
logger = logging.getLogger(__name__)

BASE = "https://httpbin.org"


# ── 1. Sync vs async — timing comparison ─────────────────
def sync_fetch(name: str) -> str:
    time.sleep(0.3)
    return f"{name} done"

async def async_fetch(name: str) -> str:
    await asyncio.sleep(0.3)
    return f"{name} done"

async def timing_comparison():
    ids = ["RBI/101", "RBI/102", "RBI/103"]

    # Sync — sequential, 3 × 0.3s = ~0.9s
    start = time.time()
    sync_results = [sync_fetch(cid) for cid in ids]
    print(f"Sync:  {time.time()-start:.2f}s — {sync_results}")

    # Async sequential — still 0.9s (wrong way to use async)
    start = time.time()
    async_seq = []
    for cid in ids:
        r = await async_fetch(cid)
        async_seq.append(r)
    print(f"Async sequential: {time.time()-start:.2f}s")

    # Async concurrent — ~0.3s (correct way)
    start = time.time()
    async_con = await asyncio.gather(
        async_fetch("RBI/101"),
        async_fetch("RBI/102"),
        async_fetch("RBI/103"),
    )
    print(f"Async concurrent: {time.time()-start:.2f}s — {async_con}")


# ── 2. async def and await basics ─────────────────────────
async def fetch_circular(cid: str, delay: float = 0.2) -> dict:
    print(f"  Starting {cid}...")
    await asyncio.sleep(delay)
    print(f"  Done    {cid}")
    return {"id": cid, "pages": 24}

async def demo_await():
    print("\n── await basics ──")
    # Sequential awaits
    r1 = await fetch_circular("RBI/101", 0.1)
    r2 = await fetch_circular("RBI/102", 0.1)
    print(f"  Sequential results: {[r['id'] for r in [r1,r2]]}")


# ── 3. asyncio.gather() ───────────────────────────────────
async def demo_gather():
    print("\n── gather() ──")
    circular_ids = ["RBI/101","RBI/102","RBI/103","RBI/104","RBI/105"]

    # gather with list unpack — the real pattern
    tasks = [fetch_circular(cid, 0.2) for cid in circular_ids]
    start = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    print(f"  {len(results)} results in {elapsed:.2f}s")
    print(f"  Order preserved: {[r['id'] for r in results]}")


# ── 4. httpx.AsyncClient — real async HTTP ────────────────
async def single_async_call():
    print("\n── httpx.AsyncClient single call ──")
    async with httpx.AsyncClient(
        base_url=BASE,
        timeout=10.0,
        headers={"X-Client": "bfsi-tools/1.0"},
    ) as client:
        r = await client.get("/get", params={"circular": "RBI-101"})
        r.raise_for_status()
        data = r.json()
        print(f"  URL:    {data['url']}")
        print(f"  Params: {data['args']}")


# ── 5. Concurrent real HTTP calls with gather() ───────────
async def fetch_one(
    client: httpx.AsyncClient, cid: str
) -> dict | None:
    try:
        r = await client.get("/get", params={"circular": cid})
        r.raise_for_status()
        return {"id": cid, "status": r.status_code}
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP {e.response.status_code} for {cid}")
        return None
    except httpx.TimeoutException:
        logger.error(f"Timeout for {cid}")
        return None


async def concurrent_http():
    print("\n── concurrent HTTP calls ──")
    circular_ids = [
        "RBI/101", "RBI/102", "RBI/103",
        "RBI/104", "RBI/105",
    ]

    async with httpx.AsyncClient(
        base_url=BASE,
        timeout=10.0,
        headers={"X-Client": "bfsi-tools/1.0"},
    ) as client:
        start = time.time()
        tasks = [fetch_one(client, cid) for cid in circular_ids]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start

    ok = [r for r in results if r]
    print(f"  {len(ok)}/{len(circular_ids)} succeeded in {elapsed:.2f}s")
    for r in ok:
        print(f"  {r['id']}: status={r['status']}")


# ── 6. AsyncBFSIClient — full async client ────────────────
class AsyncBFSIClient:
    def __init__(self, base_url: str, api_key: str):
        self.call_count = 0
        self._errors:   list[str] = []
        self._client    = httpx.AsyncClient(
            base_url=base_url,
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type":  "application/json",
                "X-Client":      "bfsi-tools/1.0",
            }
        )
        logger.info(f"AsyncBFSIClient ready — {base_url}")

    async def get(
        self, path: str, params: dict = None
    ) -> dict | None:
        self.call_count += 1
        try:
            r = await self._client.get(path, params=params)
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

    async def fetch_many(
        self, paths: list[str]
    ) -> list[dict | None]:
        """Fetch multiple paths concurrently."""
        tasks = [self.get(p) for p in paths]
        return await asyncio.gather(*tasks)

    async def close(self) -> None:
        await self._client.aclose()

    def stats(self) -> dict:
        return {
            "calls":        self.call_count,
            "errors":       len(self._errors),
            "success_rate": (
                f"{(self.call_count - len(self._errors)) / max(self.call_count,1):.0%}"
            ),
        }

    def __repr__(self) -> str:
        return (
            f"AsyncBFSIClient("
            f"calls={self.call_count}, "
            f"errors={len(self._errors)})"
        )


async def demo_async_client():
    print("\n── AsyncBFSIClient ──")
    client = AsyncBFSIClient(BASE, "demo-key")

    # Single call
    data = await client.get("/get", params={"q": "RBI-101"})
    if data:
        print(f"  Single GET: {data['args']}")

    # Batch — 5 concurrent calls
    start = time.time()
    results = await client.fetch_many(["/get"] * 5)
    elapsed = time.time() - start
    ok = sum(1 for r in results if r)
    print(f"  Batch: {ok}/5 in {elapsed:.2f}s")

    # Error path
    await client.get("/status/429")
    await client.get("/status/401")

    print(f"  Stats: {client.stats()}")
    print(f"  {client}")

    await client.close()


# ── Entry point ───────────────────────────────────────────
async def main():
    await timing_comparison()
    await demo_await()
    await demo_gather()
    await single_async_call()
    await concurrent_http()
    await demo_async_client()


if __name__ == "__main__":
    asyncio.run(main())