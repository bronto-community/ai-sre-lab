import os
import re
from pathlib import Path

import httpx2
from bedrock_agentcore import BedrockAgentCoreApp
from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

SYSTEM_PROMPT = "\n\n".join(p.read_text() for p in sorted(Path("prompts").glob("*.md")))

# #region eyes
# The eyes: Bronto's MCP server. Its tools (search logs, list datasets, ...)
# become tools the agent can call.
bronto = MCPClient(lambda: streamable_http_client(
    os.environ.get("BRONTO_MCP_URL", "https://mcp.eu.bronto.io/mcp"),
    http_client=httpx2.AsyncClient(
        headers={"X-BRONTO-API-KEY": os.environ["BRONTO_API_KEY"]}, timeout=60,
    ),
))
# #endregion

# #region code
# The code: GitHub's MCP server, read-only repository tools (files, commits, releases).
github = MCPClient(lambda: streamable_http_client(
    os.environ.get("GITHUB_MCP_URL", "https://api.githubcopilot.com/mcp/x/repos/readonly"),
    http_client=httpx2.AsyncClient(
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}, timeout=60,
    ),
))
# #endregion

model = BedrockModel(
    model_id=os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0"),
    region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION", "us-west-2"),
)
app = BedrockAgentCoreApp()


def answer(result, reasoning: bool) -> str:
    """Some models write their reasoning into the answer. Drop it unless asked."""
    text = str(result).strip()
    if reasoning or not text.startswith("<reasoning>"):
        return text
    if re.search(r"</(reasoning|analysis)>?", text):  # closed: cut at the last close tag
        return re.sub(r"(?s)^.*</(reasoning|analysis)>?", "", text).strip()
    m = re.search(r"(?m)^(\*\*|#|\|)", text)          # unclosed: cut where the answer starts
    return text[m.start():].strip() if m else text


# #region mouth
# The mouth: the hypothesis goes where humans already look, as a GitHub issue.
def file_issue(question: str, hypothesis: str) -> str:
    r = httpx2.post(
        f"https://api.github.com/repos/{os.environ.get('GITHUB_REPO', 'ai-sre-lab/storefront')}/issues",
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"},
        json={"title": f"[investigation] {question}"[:120], "body": hypothesis},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["html_url"]
# #endregion


# #region agent
@app.entrypoint
def invoke(payload: dict) -> dict:
    question = payload.get("prompt", "Hello!")
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[bronto, github])
    hypothesis = answer(agent(question), payload.get("reasoning", False))
    return {"result": file_issue(question, hypothesis)}
# #endregion


if __name__ == "__main__":
    print("""Step 7 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "Customers say checkout got slow in the last 30 minutes. What is going on?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
