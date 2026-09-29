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

<div class="n">Your <code>.env</code>, filled in as you go</div>

<EnvBlock class="env-sm" :fixed="{ AWS_DEFAULT_REGION: 'us-west-2', AWS_ACCESS_KEY_ID: '<step 1>', AWS_SECRET_ACCESS_KEY: '<step 1>', AWS_SESSION_TOKEN: '<step 1>' }" :names="['BRONTO_API_KEY', 'GITHUB_TOKEN']" />

<div class="n">Optional: nicer output</div>

<div class="opt"><code>brew install jq glow</code> <span>(or your package manager)</span></div>

<PrettyToggle class="mt-2" />

<RoomKeys />

</div>

<style>
.steps .n {
  margin: 1.2rem 0 0.4rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps li { font-size: 1.05rem; }
.steps .n code { font-size: 1em; text-transform: none; }
.env-sm { font-size: 0.7em; line-height: 1.4; }
.opt { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
.opt span { color: var(--ink-dim); }
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

<div class="n">1 · Get your lab account's AWS credentials</div>

Workshop Studio event page → **Get AWS CLI credentials** → the macOS / Linux lines

<div class="n">2 · Put them in <code>.env</code>: drop <code>export</code> and the quotes</div>

```ini
AWS_DEFAULT_REGION=us-west-2
AWS_ACCESS_KEY_ID=ASIA...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=...
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
```

<div class="hint">At home: a Bedrock API key works too, as <code>AWS_BEARER_TOKEN_BEDROCK=…</code>.</div>

<div class="n">3 · Start the agent</div>

```bash
docker run --rm -p 8080:8080 --env-file .env ghcr.io/bronto-community/ai-sre-agent:step-1
```

<div class="n">4 · Ask it something, from a second terminal</div>

<Curl prompt="Who are you?" answer="I’m Claude, an AI assistant made by Anthropic ..." />

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

Lab account credentials are temporary: if calls start failing with an expired token, fetch them again from the event page.
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

<EnvBlock :names="['BRONTO_API_KEY']" />

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

---

# Step 4 — give it a mouth

<div class="lbl">prompts/report.md</div>

<<< @/agent/step-4/prompts/report.md md

<div class="lbl">agent.py</div>

<<< @/agent/step-4/agent.py#mouth python

<<< @/agent/step-4/agent.py#agent python {5-6}

<style>
.lbl {
  margin: 0.7rem 0 0.25rem;
  font-family: 'Geist Mono', monospace; font-size: 0.7rem; color: var(--ink-dim);
}
.lbl:first-of-type { margin-top: 0; }
.slidev-layout { --slidev-code-font-size: 0.66em; }
.slidev-layout :deep(pre), .slidev-layout :deep(code), .slidev-layout :deep(.line) { white-space: pre-wrap; overflow-wrap: anywhere; }
</style>

<!--
The answer no longer comes back to you: it goes where the on-call team
already looks. One issue per question, filed by the code, not the model.
-->

---

# Step 4 — run it

<div class="steps">

<div class="n">1 · Add your GitHub token to <code>.env</code></div>

<EnvBlock :names="['GITHUB_TOKEN']" />

<div class="n">2 · Stop step 3 (Ctrl-C), start step 4</div>

```bash
docker run --rm -p 8080:8080 --env-file .env \
  -v "$PWD/my.md:/app/prompts/my.md" ghcr.io/bronto-community/ai-sre-agent:step-4
```

<div class="n">3 · Ask it, then open the issue</div>

<Curl prompt="Anything wrong with checkout?" answer="https://github.com/ai-sre-lab/storefront/issues/..." />

<div class="hint">Read the hypothesis. Is it right? How confident is it?</div>

</div>

<style>
.steps .n {
  margin: 0.9rem 0 0.35rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps .n code { font-size: 1em; text-transform: none; }
.steps p { margin: 0; }
.steps .hint { margin-top: 0.3rem; font-size: 0.85rem; color: var(--ink-dim); }
</style>

<!--
It will often be confidently wrong here: in testing it concluded checkout was
down because a query returned nothing. That's the point to build on.
-->

---

# Step 5 — better instructions

<div class="steps">

<div class="n">1 · Teach it how you investigate: add to <code>my.md</code></div>

<<< @/agent/rules.example.md md

<div class="n">2 · Restart step 4 (Ctrl-C, same command), ask again</div>

<Curl prompt="Customers say checkout got slow in the last 30 minutes. What is going on?" answer="https://github.com/ai-sre-lab/storefront/issues/..." />

<div class="hint">Better? Worse? Did it run out of context?</div>

</div>

<style>
.steps .n {
  margin: 0.9rem 0 0.35rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps .n code { font-size: 1em; text-transform: none; }
.steps p { margin: 0; }
.steps .hint { margin-top: 0.3rem; font-size: 0.85rem; color: var(--ink-dim); }
</style>

<!--
Same image, same model, different instructions. The prompt files are read at
start-up, hence the restart.

It may also fail outright: search results can exceed the model's context
(Haiku 4.5: 200k tokens, Nova Lite: 300k). Keep that for the DIY-limits discussion at the end.
-->

---

# Step 6 — better model

<div class="steps">

<div class="n">1 · Pick another model in <code>.env</code></div>

```ini
BEDROCK_MODEL_ID=us.amazon.nova-lite-v1:0
```

<div class="hint">Any Bedrock model your account can use: Bedrock console → Model catalog.</div>

<div class="n">2 · Restart step 4, ask the same question</div>

<Curl prompt="Customers say checkout got slow in the last 30 minutes. What is going on?" answer="https://github.com/ai-sre-lab/storefront/issues/..." />

<div class="hint">Compare the two issues. What changed with the model alone?</div>

</div>

<style>
.steps .n {
  margin: 0.9rem 0 0.35rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps .n code { font-size: 1em; text-transform: none; }
.steps p { margin: 0; }
.steps .hint { margin-top: 0.3rem; font-size: 0.85rem; color: var(--ink-dim); }
</style>

<!--
Same image, same instructions, different model. Instructions and model are
configuration, not code.
-->

---

# Step 7 — give it the code

<div class="lbl">prompts/code.md</div>

<<< @/agent/step-7/prompts/code.md md

<div class="lbl">agent.py</div>

<<< @/agent/step-7/agent.py#code python

<<< @/agent/step-7/agent.py#agent python {4}

<style>
.lbl {
  margin: 0.7rem 0 0.25rem;
  font-family: 'Geist Mono', monospace; font-size: 0.7rem; color: var(--ink-dim);
}
.lbl:first-of-type { margin-top: 0; }
.slidev-layout { --slidev-code-font-size: 0.66em; }
.slidev-layout :deep(pre), .slidev-layout :deep(code), .slidev-layout :deep(.line) { white-space: pre-wrap; overflow-wrap: anywhere; }
</style>

<!--
Step 4 plus one more tool source: GitHub's MCP server, read-only repository
tools only (files, commits, tags). It can't see the issues it filed earlier.
-->

---

# Step 7 — run it

<div class="steps">

<div class="n">1 · Stop step 4 (Ctrl-C), start step 7</div>

```bash
docker run --rm -p 8080:8080 --env-file .env \
  -v "$PWD/my.md:/app/prompts/my.md" ghcr.io/bronto-community/ai-sre-agent:step-7
```

<div class="n">2 · Ask again</div>

<Curl prompt="Customers say checkout got slow in the last 30 minutes. What is going on?" answer="https://github.com/ai-sre-lab/storefront/issues/..." />

<div class="hint">Does it find the deploy? Does it open the release and pick the right commit?</div>

</div>

<style>
.steps .n {
  margin: 0.9rem 0 0.35rem;
  font-family: 'Geist Mono', monospace; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em; color: var(--sapphire);
}
.steps .n:first-child { margin-top: 0.4rem; }
.steps .n code { font-size: 1em; text-transform: none; }
.steps p { margin: 0; }
.steps .hint { margin-top: 0.3rem; font-size: 0.85rem; color: var(--ink-dim); }
</style>

<!--
In testing it found the deploy marker and the commit, but stopped there. The
last hop (read every commit in the release) is a rule participants can add
to my.md.
-->

---

# What we built

<AISREArchSketch variant="lab" :stage="4" class="built-sketch" />

<div class="steps7">
  <span><b>1</b> loop</span><span><b>2</b> identity</span><span><b>3</b> eyes</span><span><b>4</b> mouth</span>
  <span><b>5</b> instructions</span><span><b>6</b> model</span><span><b>7</b> code</span>
</div>

<style>
.built-sketch { transform: scale(0.82); transform-origin: top center; margin-bottom: -3.5rem; }
.steps7 { display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap; }
.steps7 span {
  padding: 0.3rem 0.8rem; border-radius: 999px; border: 1px solid var(--border);
  background: var(--surface); font-size: 0.9rem;
}
.steps7 b { font-family: 'Geist Mono', monospace; color: var(--sapphire); margin-right: 0.25rem; }
</style>

<!--
A model, an identity, telemetry, an output, better instructions, a better
model, the code. About 80 lines of Python, and most of what mattered was prose.
-->

---

# What's next

<div class="lead">You now know what an AI SRE is and how it works. Use that to choose: <b>buy or build</b>.</div>

<div class="bb">
  <div class="col">
    <div class="k">Buy</div>
    <h3>AWS DevOps Agent, or others</h3>
    <div class="sc-list">
      <span>Solves much of what we hit today: context limits, tuning, integrations.</span>
      <span>Still extensible: custom skills, your own tools.</span>
    </div>
    <a class="wp-url" href="https://docs.aws.amazon.com/devopsagent/" target="_blank" rel="noopener">docs.aws.amazon.com/devopsagent</a>
  </div>
  <div class="col">
    <div class="k">Build</div>
    <h3>Take this skeleton further</h3>
    <div class="sc-list">
      <span>Let alerts trigger it, not curl.</span>
      <span>Run it on AgentCore Runtime: <code>agentcore deploy</code></span>
      <span>Let it watch itself: its own traces, then improve itself.</span>
      <span>More tools: cluster, cloud APIs, past incidents.</span>
    </div>
  </div>
</div>

<style>
.lead { font-size: 1.25rem; margin: 0.6rem 0 1.6rem; color: var(--ink-dim); }
.lead b { color: var(--ink); }
.bb { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
.col { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1.1rem 1.3rem; }
.col .k {
  font-family: 'Geist Mono', monospace; font-size: 0.75rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.14em; color: var(--sapphire);
}
.col h3 { margin: 0.3rem 0 0.8rem; font-size: 1.3rem; }
.col .sc-list span { color: var(--ink); font-size: 1rem; line-height: 1.4; }
.col .wp-url { display: inline-block; margin-top: 1rem; font-size: 0.95rem; }
.col code { white-space: nowrap; }
</style>

<!--
Buy: most of what hurt today (confidently wrong, context overflow, endless
tuning, wiring every tool) is what a managed agent takes off your plate. And
you can still extend it.

Build: this is a skeleton. Alerts as the trigger, AgentCore Runtime instead of
a laptop, self-monitoring feeding self-improvement, more tools.
-->

---
layout: center
class: text-center
---

<div class="thanks">
  <div class="thanks-left">
    <h1 class="thanks-title">Thank you</h1>
    <div class="thanks-links">
      <div class="tl">
        <span class="tl-label">These slides</span>
        <a class="tl-url" href="https://ote.li/ai-sre-lab" target="_blank" rel="noopener">ote.li/ai-sre-lab</a>
      </div>
      <QrCode url="https://ote.li/ai-sre-lab" :size="110" />
    </div>
  </div>

  <ThanksBronto>What would <em>your</em> agent get wrong?</ThanksBronto>
</div>

<style>
.thanks { display: flex; align-items: center; justify-content: center; gap: 3.5rem; text-align: left; }
.thanks-title { font-size: 4rem; line-height: 1.05; }
.thanks-links { display: flex; align-items: center; gap: 1.4rem; margin-top: 1.8rem; }
.tl { display: flex; flex-direction: column; align-items: flex-start; gap: 0.1rem; }
.tl-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--ink-dim); }
.thanks em { font-style: italic; color: var(--sapphire); }
.thanks .tl-url { white-space: nowrap; }
</style>

