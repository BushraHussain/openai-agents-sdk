from agents import Agent, Runner, function_tool, RunContextWrapper, enable_verbose_stdout_logging
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

@dataclass
class UserInfo:
    user_id: str
    user_name: str
    user_plan: str
    user_purchase_history: list
    balance: float

@function_tool
async def get_user_balance(wrapper: RunContextWrapper[UserInfo]):
    return f"User ID {wrapper.context.user_id} has a balance of ${wrapper.context.balance}"

async def main():
    user = UserInfo(
        user_id="12345",
        user_name="Bushra Malik",
        user_plan="Premium",
        user_purchase_history=["credit card", "car loan"],
        balance=100000
    )

    agent = Agent[UserInfo](
        name="Customer Support Agent",
        instructions=lambda ctx: (
            f"You are a helpful assistant. The user's name is {ctx.user_name} and "
            f"they are on the {ctx.user_plan} plan. Be polite. Only provide the user's balance if asked."
        ),
        tools=[get_user_balance],
    )

    response = await Runner.run(
        starting_agent=agent,
        input="What is the balance of the user?",
        context=user,
    )

    print(response.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
