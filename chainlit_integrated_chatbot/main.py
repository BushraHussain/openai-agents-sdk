import chainlit as cl
from agents import Agent, Runner 

# Create a new agent
agent:Agent = Agent(
    name="chatbot agent",
    instructions="You're a chatbot agent for customer service"
)

# response = Runner.run_sync(
#     agent,
#     "hi, who are you?"
# )

# print(f"Response : {response.final_output}")

# @cl.on_message
# async def main(message:cl.Message):
#     await cl.Message(
#         content = f"received message: {message.content}"
#     ).send()

@cl.on_message
async def main(message:cl.Message):

    response = Runner.run_sync(
        agent,
        message.content
    )

    await cl.Message(
        content = f"Agent: {response.final_output}"
    ).send()