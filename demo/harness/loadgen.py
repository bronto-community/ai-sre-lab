"""Steady customer traffic. Concurrency is what makes the system interesting."""

import asyncio
import logging
import os
import random
import time

import httpx

CONCURRENCY = int(os.environ.get("CONCURRENCY", "20"))
RPS = float(os.environ.get("TARGET_RPS", "20"))
WEB = os.environ.get("WEB_URL", "http://web:8000")

logging.basicConfig(level=logging.INFO, format="%(asctime)s loadgen %(levelname)s %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("loadgen")

stats = {"ok": 0, "err": 0, "latency": []}


async def customer(client: httpx.AsyncClient) -> None:
    started = time.monotonic()
    try:
        await client.get(f"{WEB}/browse")
        r = await client.post(f"{WEB}/checkout")
        stats["ok" if r.status_code == 200 else "err"] += 1
    except Exception:  # noqa: BLE001 - a failed checkout is data, not a crash
        stats["err"] += 1
    stats["latency"].append((time.monotonic() - started) * 1000)


async def report() -> None:
    while True:
        await asyncio.sleep(15)
        lat = sorted(stats["latency"])
        stats["latency"] = []
        if not lat:
            continue
        total = stats["ok"] + stats["err"]
        log.info("%d requests, %.1f%% errors, p95 %.0fms",
                 total, 100 * stats["err"] / max(total, 1), lat[int(len(lat) * 0.95) - 1])
        stats["ok"] = stats["err"] = 0


async def main() -> None:
    log.info("%d concurrent customers, ~%.0f rps", CONCURRENCY, RPS)
    asyncio.create_task(report())
    async with httpx.AsyncClient(timeout=20.0, limits=httpx.Limits(max_connections=CONCURRENCY * 2)) as c:
        while True:
            await asyncio.gather(*(customer(c) for _ in range(CONCURRENCY)))
            await asyncio.sleep(max(0.0, CONCURRENCY / RPS - 0.1) * random.uniform(0.8, 1.2))


if __name__ == "__main__":
    asyncio.run(main())
