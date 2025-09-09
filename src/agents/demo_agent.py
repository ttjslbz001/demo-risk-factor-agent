from strands import Agent
from strands.models.openai import OpenAIModel
from strands_tools import calculator

model = OpenAIModel(
    client_args={
        "api_key": "********",
        "base_url": "https://us-ailab-api.telenav.com/v1",
    },
    # **model_config
    model_id="claude3.5-bedrock",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

agent = Agent(model=model, tools=[calculator])
response = agent("What is 2+2")
print(response)