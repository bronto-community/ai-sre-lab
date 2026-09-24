# Plan

Attendees follow the lab slides on their own machine and copy commands from them.
Each step is a prebuilt image: `ghcr.io/bronto-community/ai-sre-agent:step-N`.

1. **Loop**: bare agent in a container, `curl` it. *(`step-1`)*
2. **Identity**: SRE prompt from `prompts/*.md`, plus your own `my.md`. Says it has no telemetry. *(`step-2`)*
3. **Eyes**: Bronto MCP. "What services do you know?", "anything wrong with X at Y?" *(`step-3`)*
4. **Mouth**: files its hypothesis as a GitHub issue; the reply is the link. May well be wrong. *(`step-4`)*
5. **Better instructions**: rules in `my.md` (look for slowness, baselines, deploy markers). *(same image)*
6. **Better model**: a different `BEDROCK_MODEL_ID`. *(same image)*
7. **Code**: GitHub MCP, read-only repository tools; now it can name the commit. *(`step-7`)*

## Environment

- `ai-sre-lab/storefront` (public, machine user): app code + issues. Built from `storefront-src/`.
- One EC2 `t4g.small` runs the app with `demo/`; a push to storefront deploys it (OIDC + SSM).
- Reset/release: `workflow_dispatch` here, pushes storefront to the initial / release commits.

Parked: agent telemetry.
