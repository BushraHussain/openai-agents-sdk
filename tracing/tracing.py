from agents import Agent, Runner, trace
from dotenv import load_dotenv
from agents.run import RunConfig

load_dotenv()

# ------------------ Agent Configuration -------------------
python_agent = Agent(
    name="Python Agent",
    instructions="You are a Python expert. Answer questions about Python programming."
)

# ------------------ Running agent inside main fuction ------

async def main():

    # Secure config: No sensitive data will be logged
    secure_config = RunConfig(trace_include_sensitive_data=False)

    # Multiple calls to run() in a single trace / single workflow - Higher level traces 
    with trace("Python Agent Workflow"):
        # First call to the agent
        result = await Runner.run(
            python_agent,
            "What is a function in Python just in 2 lines?",
            run_config = secure_config # Secure config to avoid sensitive data logging
        )

        # Second call to the agent
        result_two = await Runner.run(
            python_agent,
            f"{result.final_output} Can you give me an example of a function?",
            # run_config=secure_config  # let's comment it to see the difference in openai trace dashboard
        )

        print(f"Result 1: {result.final_output} ")
        print(f"Result 2: {result_two.final_output} ")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
