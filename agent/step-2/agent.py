import os
import re
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


def answer(result, reasoning: bool) -> str:
    """gpt-oss sometimes writes its reasoning into the answer. Drop it unless asked."""
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
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT)
    return {"result": answer(agent(payload.get("prompt", "Hello!")), payload.get("reasoning", False))}
# #endregion


if __name__ == "__main__":
    print("""Step 2 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "Checkout is slow. What is wrong?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
