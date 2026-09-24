# Plan

Attendees follow the lab slides on their own machine and copy commands from them.
Each step is a prebuilt image: `ghcr.io/bronto-community/ai-sre-agent:step-N`.

1. **Loop** — bare agent in a container, `curl` it. *(built: `agent/step-1`)*
2. **Identity** — SRE system prompt from `prompts/*.md`. Asked to investigate, it says it has no telemetry. *(built: `agent/step-2`)*
3. **Bronto MCP** — "what services do you know?", then "anything wrong with X at Y?" *(built: `agent/step-3`)*
4. **GitHub MCP** — reads the source; same question now names the release.
5. **Issue** — files a GitHub issue; the reply is a link to it.

## Environment

- `ai-sre-lab/storefront` (public, machine user): app code + issues. Built from `storefront-src/`.
- One EC2 `t4g.small` runs the app with `demo/`; a push to storefront deploys it (OIDC + SSM).
- Reset/release: `workflow_dispatch` here, pushes storefront to the initial / release commits.

Parked: agent telemetry.
