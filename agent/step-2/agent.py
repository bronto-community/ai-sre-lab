import os
from pathlib import Path

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

# #region identity
# The identity: every file in prompts/ becomes part of the system prompt.
SYSTEM_PROMPT = "\n\n".join(p.read_text() for p in sorted(Path("prompts").glob("*.md")))
# #endregion

model = BedrockModel(
    model_id=os.environ.get("BEDROCK_MODEL_ID", "openai.gpt-oss-120b-1:0"),
    region_name=os.environ.get("AWS_REGION", "eu-central-1"),
)
app = BedrockAgentCoreApp()


# #region agent
@app.entrypoint
def invoke(payload: dict) -> dict:
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT)
    return {"result": str(agent(payload.get("prompt", "Hello!")))}
# #endregion


if __name__ == "__main__":
    print("""Step 2 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "Checkout is slow. What is wrong?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
