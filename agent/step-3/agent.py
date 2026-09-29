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

model = BedrockModel(
    model_id=os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0"),
    region_name=os.environ.get("AWS_REGION", "us-west-2"),
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


# #region agent
@app.entrypoint
def invoke(payload: dict) -> dict:
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[bronto])
    return {"result": answer(agent(payload.get("prompt", "Hello!")), payload.get("reasoning", False))}
# #endregion


if __name__ == "__main__":
    print("""Step 3 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "What services do you know about?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
