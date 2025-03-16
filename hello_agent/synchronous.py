import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

# ------------------ Gemini configuration -------------------

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# ------------------ Agent  -------------------

# define the agent 
agent:Agent = Agent(
    name="Math mentor",
    instructions="You are a helpful math teacher",
    model=model
)

# Run the agent synchronously using run_sync
result = Runner.run_sync(
    agent, 
    "hi who are you?",
    run_config=config
)

print("\nCALLING AGENT\n")
print("Agent response:", result.final_output)

