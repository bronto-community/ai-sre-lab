"""payments-gateway -- our side of the PSP integration."""

import asyncio
import logging
import os

import httpx
from fastapi import FastAPI

from services.common import telemetry

app = FastAPI(title="payments-gateway")
telemetry.setup(app)
log = logging.getLogger("payments-gateway")

PSP_URL = os.environ.get("PSP_URL", "http://psp:8000")
SETTLEMENT_MS = int(os.environ.get("SETTLEMENT_MS", "20"))

client = httpx.AsyncClient(timeout=5.0)


@app.on_event("startup")
async def startup() -> None:
    telemetry.announce_release()


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}


@app.post("/charge")
async def charge(req: dict) -> dict:
    # Ledger write before we ask the PSP for an authorisation.
    await asyncio.sleep(SETTLEMENT_MS / 1000.0)
    payload = dict(req, merchant_ref=os.environ.get("MERCHANT_REF", "storefront-eu"))
    r = await client.post(f"{PSP_URL}/authorize", json=payload)
    return {"authorized": True, "psp": r.json()}
