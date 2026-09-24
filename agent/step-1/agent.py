import os
import re

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id=os.environ.get("BEDROCK_MODEL_ID", "openai.gpt-oss-120b-1:0"),
    region_name=os.environ.get("AWS_REGION", "eu-central-1"),
)
app = BedrockAgentCoreApp()


def answer(result, reasoning: bool) -> str:
    """gpt-oss sometimes writes its reasoning into the answer. Drop it unless asked."""
    text = str(result)
    return text if reasoning else re.sub(r"(?s)^.*</(reasoning|analysis)>?", "", text).strip()


@app.entrypoint
def invoke(payload: dict) -> dict:
    agent = Agent(model=model)
    return {"result": answer(agent(payload.get("prompt", "Hello!")), payload.get("reasoning", False))}


if __name__ == "__main__":
    print("""Step 1 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "Who are you?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
