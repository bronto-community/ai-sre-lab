import os
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
    model_id=os.environ.get("BEDROCK_MODEL_ID", "openai.gpt-oss-120b-1:0"),
    region_name=os.environ.get("AWS_REGION", "eu-central-1"),
)
app = BedrockAgentCoreApp()


# #region agent
@app.entrypoint
def invoke(payload: dict) -> dict:
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[bronto])
    return {"result": str(agent(payload.get("prompt", "Hello!")))}
# #endregion


if __name__ == "__main__":
    print("""Step 3 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "What services do you know about?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
