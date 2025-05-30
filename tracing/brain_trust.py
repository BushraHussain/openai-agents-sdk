# BrainTrust is External Trace Processor for OpenAI Agents
# First we need to create an account on Braintrust 
# Get an API key & set it as an environment variable. BRAINTRUST_API_KEY=..
# Install the required packages: "uv add braintrust"
# Add the following code. 

import asyncio
from dotenv import load_dotenv
# "set_trace_processors" lets you replace the default processors with your own trace processor 
# OR external processor e.g. Braintrust
from agents import Agent, Runner, set_trace_processors 
from braintrust import init_logger
from braintrust.wrappers.openai import BraintrustTracingProcessor
 
load_dotenv()
 
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
    )
 
    result = await Runner.run(agent, "Tell me about loops in programming.")
    print(result.final_output)
 
 
if __name__ == "__main__":
    # If you comment out below line, the default "Batch Trace Processor" will be used that is
    # sending the traces to the OpenAi Backend.
    set_trace_processors([BraintrustTracingProcessor(init_logger("openai-agent"))])
    asyncio.run(main())