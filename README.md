# AI SRE lab

Build your own AI SRE with AgentCore. Hands-on lab for the AWS + Bronto evening.

| Path | What |
|---|---|
| [`slides/`](slides/) | the lab deck (Vercel) |
| [`agent/`](agent/) | `base` (Python + libraries) and one thin image per step, `ghcr.io/bronto-community/ai-sre-agent:step-N` |
| [`storefront-src/`](storefront-src/), [`build-storefront.sh`](build-storefront.sh) | source for the demo app repo, `ai-sre-lab/storefront` |
| [`demo/`](demo/) | load generator, payment-processor mock, collector |
| [`infra/aws.yml`](infra/aws.yml) | the AWS stack: one EC2 host, GitHub OIDC roles |
| [`PLAN.md`](PLAN.md) | the steps |

## Operating the shop

- **Actions → lab → reset**: storefront `main` back to v3.1.0 (healthy).
- **Actions → lab → release**: storefront `main` to v3.2.0, which ships the fault.
- **Actions → harness**: re-ship `demo/` to the host (runs on every push to `demo/`).

Every push to storefront `main` deploys through its own `deploy` workflow.

Internal until after the event: it contains the incident.

## License

Content under [CC BY 4.0](LICENSE), code under [MIT](LICENSE-CODE). No trademark
rights; see [NOTICE](NOTICE).
