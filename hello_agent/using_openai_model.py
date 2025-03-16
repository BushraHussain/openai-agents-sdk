from agents import Agent, Runner
import os
from dotenv import load_dotenv

load_dotenv()

# Load the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")

agent:Agent = Agent(
    name="Chemistry Teacher",
    instructions="You're a helpful chemistry teacher that helps students with their homework.",
)

response = Runner.run_sync(
    agent,
    "Hi, who are you?"
)

print(f"Agent Response: {response.final_output}")



