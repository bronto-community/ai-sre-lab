"""checkout-api -- turns a cart into a confirmed order."""

import asyncio
import logging

import httpx
from fastapi import FastAPI

from services.checkout import config
from services.common import telemetry

app = FastAPI(title="checkout-api")
telemetry.setup(app)
log = logging.getLogger("checkout-api")

client = httpx.AsyncClient(
    timeout=config.PAYMENTS_TIMEOUT_S,
    limits=httpx.Limits(
        max_connections=config.PAYMENTS_POOL_SIZE,
        max_keepalive_connections=config.PAYMENTS_POOL_SIZE,
    ),
)


@app.on_event("startup")
async def startup() -> None:
    telemetry.announce_release()


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}


@app.post("/checkout")
async def checkout(order: dict) -> dict:
    await asyncio.sleep(config.ORDER_ASSEMBLY_MS / 1000.0)
    r = await client.post(f"{config.PAYMENTS_URL}/charge", json={"amount": 4200})
    r.raise_for_status()
    return {"status": "confirmed", "payment": r.json()}
