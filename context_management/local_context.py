from agents import Agent, Runner, RunContextWrapper, enable_verbose_stdout_logging,function_tool 
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

@dataclass
class UserContext:
    user_name:str
    user_id:int


@function_tool
async def fetch_user_age(wrapper:RunContextWrapper[UserContext]) -> str:
    return f"User {wrapper.context.user_name} is 30 years old."

async def main():
    new_user_context = UserContext(
        user_name="Alice",
        user_id=12345
    )

    agent = Agent(
        name="Math agent",
        instructions="You are a math agent. You can solve math problems and answer questions related to mathematics.",
        tools=[fetch_user_age]
    )
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=new_user_context
    )

    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())