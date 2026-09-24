"""catalog-api -- product listings."""

import asyncio
import logging
import os
import random

from fastapi import FastAPI

from services.common import telemetry

app = FastAPI(title="catalog-api")
telemetry.setup(app)
log = logging.getLogger("catalog-api")

LOOKUP_MS = int(os.environ.get("LOOKUP_MS", "10"))


@app.on_event("startup")
async def startup() -> None:
    telemetry.announce_release()


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}


@app.get("/items")
async def items() -> dict:
    await asyncio.sleep(LOOKUP_MS / 1000.0)
    if random.random() < 0.1:
        log.warning("slow query detected: %dms on catalog_items", random.randint(700, 900))
    if random.random() < 0.3:
        log.warning("cache miss for shard %d, falling back to primary", random.randint(1, 8))
    return {"items": ["sku-1", "sku-2", "sku-3"]}
