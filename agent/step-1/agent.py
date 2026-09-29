import os
import re

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

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


@app.entrypoint
def invoke(payload: dict) -> dict:
    agent = Agent(model=model)
    return {"result": answer(agent(payload.get("prompt", "Hello!")), payload.get("reasoning", False))}


if __name__ == "__main__":
    print("""Step 1 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "Who are you?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
