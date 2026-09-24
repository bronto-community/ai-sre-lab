import os

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id=os.environ.get("BEDROCK_MODEL_ID", "openai.gpt-oss-120b-1:0"),
    region_name=os.environ.get("AWS_REGION", "eu-central-1"),
)
app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload: dict) -> dict:
    agent = Agent(model=model)
    return {"result": str(agent(payload.get("prompt", "Hello!")))}


if __name__ == "__main__":
    print("""Step 1 agent running, try: curl -s localhost:8080/invocations -d '{"prompt": "Who are you?"}'""", flush=True)
    app.run()  # POST /invocations, GET /ping on :8080
