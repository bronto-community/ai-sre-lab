# storefront

The four services behind the shop.

| Service | Path | Owner |
|---|---|---|
| `storefront-web` | `services/web` | Web |
| `checkout-api` | `services/checkout` | Payments |
| `payments-gateway` | `services/payments` | Payments |
| `catalog-api` | `services/catalog` | Catalog |

All four build from the root `Dockerfile`. `SERVICE_MODULE` picks the app,
`SERVICE_NAME` sets the telemetry service name.

Payment authorisation is handled by our PSP, which is external and which we
do not instrument.
