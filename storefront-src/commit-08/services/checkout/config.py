"""Runtime configuration for checkout-api."""

import os

# Outbound HTTP connection pool for the payments-gateway client.
# Reduced from 20: idle keepalive connections were the bulk of the pod's
# resident memory, and the gateway is comfortable with far fewer. PLAT-4471
PAYMENTS_POOL_SIZE = int(os.environ.get("PAYMENTS_POOL_SIZE", "2"))

# Time spent assembling the order before the charge is attempted.
ORDER_ASSEMBLY_MS = int(os.environ.get("ORDER_ASSEMBLY_MS", "15"))

PAYMENTS_URL = os.environ.get("PAYMENTS_URL", "http://payments:8000")
PAYMENTS_TIMEOUT_S = float(os.environ.get("PAYMENTS_TIMEOUT_S", "10"))
