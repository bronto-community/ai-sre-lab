"""Steady customer traffic: CUSTOMERS shoppers, each buying, then pausing.

A fixed population (closed loop) can't overload the shop: when it slows down,
shoppers wait for their orders and send less. A capacity limit shows up as
longer orders, not as a collapse.
"""

import asyncio
import logging
import os
import random
import time

import httpx

CUSTOMERS = int(os.environ.get("CUSTOMERS", "20"))
THINK_S = float(os.environ.get("THINK_S", "0.5"))
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


async def shopper(client: httpx.AsyncClient) -> None:
    while True:
        await customer(client)
        await asyncio.sleep(random.expovariate(1 / THINK_S))


async def main() -> None:
    log.info("%d shoppers, ~%.1fs between orders", CUSTOMERS, THINK_S)
    asyncio.create_task(report())
    async with httpx.AsyncClient(timeout=20.0, limits=httpx.Limits(max_connections=CUSTOMERS * 2)) as c:
        await asyncio.gather(*(shopper(c) for _ in range(CUSTOMERS)))


if __name__ == "__main__":
    asyncio.run(main())
