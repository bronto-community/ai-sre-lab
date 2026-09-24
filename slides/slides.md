---
theme: default
title: Observability for AI
info: |
  ## Observability for AI — Build your own AI SRE with AgentCore
  Hands-on lab: five steps, one live incident. Build an investigating agent on
  Amazon Bedrock AgentCore, part of the AWS + Bronto AI & Observability evening.
colorSchema: light
transition: slide-left
mdc: true
class: text-left
favicon: /img/bronto-dino.png
fonts:
  sans: Radio Canada Big
  serif: Source Serif 4
  mono: Geist Mono
---

<div class="title-hero">
  <img src="/img/confetti-left.png" class="confetti c-left" />
  <img src="/img/confetti-right.png" class="confetti c-right" />

# Observability for AI

</div>

<div class="subtitle">Build your own AI SRE with AgentCore</div>

<a href="https://bronto.io" target="_blank" rel="noopener" class="abs-bl m-10 brand-logo-link">
  <img src="/img/bronto-logo.webp" class="brand-logo" />
</a>

<style>
.title-hero { position: relative; display: inline-block; }
.title-hero h1 { font-size: 4.1rem; line-height: 1.02; }
.confetti { position: absolute; width: 118px; height: auto; pointer-events: none; }
.c-left { top: -100px; left: -60px; }
.c-right { top: 50%; right: -132px; transform: translateY(-50%); }

.subtitle { margin-top: 1.6rem; font-size: 1.3rem; color: var(--ink-dim); }
.brand-logo { width: 150px; height: auto; }

.brand-logo-link { display: inline-block; line-height: 0; transition: opacity 0.15s ease; }
.brand-logo-link:hover { opacity: 0.7; }
</style>

<!--
Put this up while people sit down. If setup already happened before the
session, skip past the setup slide when you get to it.
-->

---

# What is an AI SRE?

<AISREArchSketch :stage="4" class="mt-2" />

<div class="arch-verdict">An agentic loop for incident response.</div>

<style>
.arch-verdict {
  margin-top: 0.6rem; text-align: center;
  font-family: 'Source Serif 4', Georgia, serif; font-size: 1.6rem; color: var(--sapphire);
}
</style>

<!--
Walk through it: inputs on the left, the LLM in the middle, tools (mostly MCP)
underneath, outputs on the right. Nothing exotic, it's an agent like any other,
pointed at production.
-->


---
layout: center
---

<div class="dop">
  <div class="dop-body">
    <div class="kicker">Ready to use</div>
    <h1 class="dop-head">AWS DevOps Agent</h1>
    <div class="sc-list dop-list">
      <span>The managed version of that picture, from AWS.</span>
      <span>Starts investigating <b>the moment an alert fires</b> and comes back with a root cause and mitigation steps.</span>
      <span>Connects to the tools you already run: CloudWatch, Datadog, Splunk, Grafana, GitHub, GitLab, PagerDuty, Slack and more.</span>
    </div>
    <a class="wp-url dop-url" href="https://aws.amazon.com/devops-agent/" target="_blank" rel="noopener">aws.amazon.com/devops-agent</a>
  </div>
  <QrCode url="https://aws.amazon.com/devops-agent/" :size="150" caption="try it" />
</div>

<style>
.dop { display: flex; align-items: center; gap: 3.5rem; }
.dop-body { max-width: 38rem; }
.kicker {
  font-family: 'Geist Mono', monospace; font-size: 0.85rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.16em; color: var(--sapphire);
}
.dop-head { font-size: 3rem; margin: 0.5rem 0 1.5rem; }
.dop-list span { color: var(--ink); font-size: 1.1rem; line-height: 1.4; }
.dop-url { display: inline-block; margin-top: 1.6rem; font-size: 1.1rem; }
</style>

<!--
Respectful and short. If you want an AI SRE on Monday, this is the one to try.
It's the one mention of the managed product until the close.
-->


---
layout: center
---

<div class="why">
  <div class="kicker">So why build one?</div>
  <h1 class="why-head">Tonight we build our own, on AgentCore.</h1>

  <div class="ev">
    <div class="ev-card">
      <div class="i-lucide-hand ev-icon" />
      <b>Get a feel for it</b>
      <span>What an AI SRE actually is, once you've put one together yourself.</span>
    </div>
    <div class="ev-card">
      <div class="i-lucide-cog ev-icon" />
      <b>See how it works</b>
      <span>Where the answers come from, and why it goes wrong when it does.</span>
    </div>
    <div class="ev-card">
      <div class="i-lucide-target ev-icon" />
      <b>Use it better</b>
      <span>Knowing what's inside is how you get good results from any of them, managed or your own.</span>
    </div>
  </div>
</div>

<style>
.why { max-width: 58rem; }
.kicker {
  font-family: 'Geist Mono', monospace; font-size: 0.85rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.16em; color: var(--sapphire);
}
.why-head { font-size: 2.7rem; margin: 0.6rem 0 2rem; }
.ev { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1rem; }
.ev-card {
  display: flex; flex-direction: column; gap: 0.5rem;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 14px; padding: 1.1rem 1.15rem;
}
.ev-icon { font-size: 1.5rem; color: var(--sapphire); }
.ev-card b { font-size: 1.1rem; }
.ev-card span { font-size: 0.95rem; color: var(--ink-dim); line-height: 1.4; }
</style>

<!--
Not "don't use DevOps Agent". Building one by hand is the fastest way to learn
what's in it, and what it can't see. That makes you better at using whichever
one you end up running.
-->


---

# What we'll build tonight

<AISREArchSketch variant="lab" :stage="4" class="mt-6" />

<!--
The same picture, cut down to what fits in 45 minutes: you ask it, it runs on
AgentCore, it reads telemetry through Bronto MCP and code through GitHub MCP,
and it files a GitHub issue with what it found.
-->

---

# Before you start

<div class="steps">

<div class="n">Required</div>

- **Docker**: Docker Desktop, OrbStack, Colima or Docker Engine. Check with `docker run --rm hello-world`
- **A terminal**
- **These slides**, open on your machine: [ote.li/ai-sre-lab](https://ote.li/ai-sre-lab)

<div class="n">Optional: nicer output</div>

```bash
brew install jq glow        # or your package manager
```

<PrettyToggle class="mt-4" />

</div>

<style>
.steps .n {
  margin: 1.2rem 0 0.4rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps li { font-size: 1.05rem; }
</style>

<!--
The checkbox is stored in the viewer's browser. When ticked, every curl on the
later slides pipes through `jq -r .result | glow -`.
-->

---

# Step 1 — the agent

<div>

<<< @/agent/step-1/agent.py python

</div>

<style>
.slidev-layout { --slidev-code-font-size: 0.72em; --slidev-code-line-height: 1.4; }
.slidev-layout :deep(pre), .slidev-layout :deep(code), .slidev-layout :deep(.line) { white-space: pre-wrap; overflow-wrap: anywhere; }
.slidev-layout h1 { font-size: 2rem; margin-bottom: 0.4rem; }
</style>

<!--
Pulled straight from agent/step-1/agent.py, so it never drifts.
Strands agent + AgentCore app: an HTTP endpoint around a model. Nothing else.
-->

---

# Step 1 — run an agent

<div class="steps">

<div class="n">1 · Get a Bedrock key</div>

[Bedrock playground](https://console.aws.amazon.com/bedrock/home?#/playground) → **Select model** → **gpt-oss-120b** → **Apply** → **Build** → **Generate short-term API key**

<div class="n">2 · Create a <code>.env</code> file with the key, its region and a model</div>

```ini
AWS_REGION=eu-central-1
AWS_BEARER_TOKEN_BEDROCK=...
BEDROCK_MODEL_ID=openai.gpt-oss-120b-1:0
```

<div class="hint">Any Bedrock model works. We use gpt-oss for now.</div>

<div class="n">3 · Start the agent</div>

```bash
docker run --rm -p 8080:8080 --env-file .env ghcr.io/bronto-community/ai-sre-agent:step-1
```

<div class="n">4 · Ask it something, from a second terminal</div>

<Curl prompt="Who are you?" answer="I’m ChatGPT, an AI language model created by OpenAI ..." />

</div>

<style>
.steps .n {
  margin: 1rem 0 0.35rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps .n code { font-size: 1em; text-transform: none; }
.steps p { margin: 0; }
.steps .hint { margin-top: 0.3rem; font-size: 0.85rem; color: var(--ink-dim); }
</style>

<!--
A model behind an endpoint. No identity, no tools.
Ctrl-C stops the agent.

The key only works in the region it was generated in, and lasts at most 12h.
-->

---

# Step 2 — give it an identity

<div class="lbl">prompts/role.md</div>

<<< @/agent/step-2/prompts/role.md md

<div class="lbl">prompts/rules.md</div>

<<< @/agent/step-2/prompts/rules.md md

<div class="lbl">agent.py</div>

<<< @/agent/step-2/agent.py#identity python

<<< @/agent/step-2/agent.py#agent python {3}

<style>
.slidev-layout { --slidev-code-font-size: 0.72em; }
.lbl {
  margin: 0.7rem 0 0.25rem;
  font-family: 'Geist Mono', monospace; font-size: 0.7rem; color: var(--ink-dim);
}
.lbl:first-of-type { margin-top: 0; }
.slidev-layout :deep(pre), .slidev-layout :deep(code), .slidev-layout :deep(.line) { white-space: pre-wrap; overflow-wrap: anywhere; }
</style>

<!--
Same agent as step 1. The only change: everything in prompts/ becomes the
system prompt.
-->

---

# Step 2 — run it

<div class="steps">

<div class="n">1 · Add your own rules: create <code>my.md</code></div>

```md
- Answer in at most three bullet points.
- End every answer with your confidence: low, medium or high.
- Sign off as "your friendly on-call dino".
```

<div class="n">2 · Stop step 1 (Ctrl-C), start step 2 with your file mounted in</div>

```bash
docker run --rm -p 8080:8080 --env-file .env \
  -v "$PWD/my.md:/app/prompts/my.md" ghcr.io/bronto-community/ai-sre-agent:step-2
```

<div class="n">3 · Ask it to investigate</div>

<Curl prompt="Checkout is slow. What is wrong?" answer="- No telemetry access yet ... Confidence: low — your friendly on-call dino" />

</div>

<style>
.steps .n {
  margin: 1rem 0 0.35rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps .n code { font-size: 1em; text-transform: none; }
</style>

<!--
It knows what it is now, and it is honest that it can't see anything.
That is the setup for step 3.

my.md lands next to role.md and rules.md; every *.md in prompts/ is loaded.
-->

---

# Step 3 — give it eyes

<<< @/agent/step-3/agent.py#eyes python

<<< @/agent/step-3/agent.py#agent python {3}

<div class="full">Full file: <code>agent/step-3/agent.py</code></div>

<style>
.full { margin-top: 0.8rem; font-size: 0.85rem; color: var(--ink-dim); }
</style>

<!--
Step 2 plus one tool source: Bronto's MCP server. The agent can now search
logs, list datasets, run saved searches, summarise errors.
-->

---

# Step 3 — run it

<div class="steps">

<div class="n">1 · Add your Bronto key to <code>.env</code></div>

```ini
BRONTO_API_KEY=...
```

<div class="n">2 · Stop step 2 (Ctrl-C), start step 3</div>

```bash
docker run --rm -p 8080:8080 --env-file .env \
  -v "$PWD/my.md:/app/prompts/my.md" ghcr.io/bronto-community/ai-sre-agent:step-3
```

<div class="n">3 · Ask what it can see</div>

<Curl prompt="What services do you know about?" answer="- checkout, payments, catalog, web ..." />

<div class="n">4 · Ask it to investigate</div>

<Curl prompt="Anything wrong with checkout?" answer="- p95 latency up since ... Confidence: medium — your friendly on-call dino" />

</div>

<style>
.steps .n {
  margin: 0.9rem 0 0.35rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps .n code { font-size: 1em; text-transform: none; }
</style>

<!--
Example answers are placeholders until the storefront app runs in the account.
-->

