"""Stand-in for the third-party payment processor.

Deliberately NOT instrumented: no OpenTelemetry, no spans, no metrics. We do
not get to instrument other people's systems, and the exercise depends on that
being genuinely true rather than merely pretended.
"""

import asyncio
import logging
import os

from fastapi import FastAPI

app = FastAPI(title="psp")
logging.basicConfig(level=logging.INFO, format="%(asctime)s psp %(levelname)s %(message)s")

LATENCY_MS = int(os.environ.get("PSP_LATENCY_MS", "30"))


@app.post("/authorize")
async def authorize(req: dict) -> dict:
    await asyncio.sleep(LATENCY_MS / 1000.0)
    return {"auth_code": "psp-ok"}
