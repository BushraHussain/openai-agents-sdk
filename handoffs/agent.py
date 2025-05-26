from agents import Agent, Runner, handoff, RunContextWrapper, enable_verbose_stdout_logging 
from dotenv import load_dotenv

load_dotenv()

enable_verbose_stdout_logging()

#------------ Define specialized agents --------

# Agent 1: Math agent
math_agent:Agent = Agent(
    name="Math mentor",
    instructions="You are a helpful math teacher who can assist with solving math problems and explaining concepts clearly.",
)

# Agent 2: Science Agent
science_agent:Agent = Agent(
    name="Science mentor",
    instructions="You are a knowledgeable science teacher who can help with scientific concepts and experiments.",
)

# Agent 3: Python Programming Agent
programming_agent:Agent = Agent(
    name="Python Programming mentor",
    instructions="You are a skilled python programming teacher who can assist with coding problems and explain programming concepts related to python.",
)


#------------ Define handoff rules for programming agent --------

def on_handoff(agent_context:RunContextWrapper[None]): # it takes two parameters, the agent context and the LLM generated inputs 
    print(f"Handoff called :: {agent_context}")


programming_agent_handoff = handoff(
    agent=programming_agent,
    tool_name_override="customized_transfer_to_python_mentor",
    tool_description_override="customized - This handoff transfers the task to a specialized Python programming mentor who can provide detailed coding assistance.",
    on_handoff = on_handoff,
)


# Agent 4: Task Assigner Agent
task_assigner_agent:Agent = Agent(
    name="Task Assigner",
    instructions="You are a task assigner who can delegate tasks to other agents based on their expertise.",
    handoffs = [math_agent, science_agent, programming_agent_handoff]
)

# ------------- Run the Task Assigner Agent --------------

async def main():
    # Run the task assigner agent with a sample task
    result = await Runner.run(
        task_assigner_agent,
        "Define list in python?",
    )

    print("\n-------CALLING TASK ASSIGNER AGENT--------\n")
    print("Task Assigner Agent response:", result.final_output)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())



