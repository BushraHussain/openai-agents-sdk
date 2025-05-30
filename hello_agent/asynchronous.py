from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
base_url ="https://generativelanguage.googleapis.com/v1beta/openai/"

# Make a client - if using a model other than openai models 
client = AsyncOpenAI(
    api_key=gemini_key,  # Pass as keyword argument
    base_url=base_url   # Pass as keyword argument
)

async def main():

    gemini_agent = Agent(
        name="Gemini Agent",
        instructions="You are a helpful assistant that can answer questions and provide information about france country.",
        model=OpenAIChatCompletionsModel(
            openai_client=client,
            model="gemini-2.0-flash",
        )
    )

    result = await Runner.run(
        gemini_agent,
        "What is the capital of France?",
    )

    print(result.final_output)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())