from agents import Agent, Runner, handoff, RunContextWrapper, enable_verbose_stdout_logging 
from agents.extensions import handoff_filters
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.run import RunConfig
from pydantic import BaseModel
from dotenv import load_dotenv
import datetime

load_dotenv()

enable_verbose_stdout_logging()
RunConfig.tracing_disabled = True

#------------ Define specialized agents & their customized handoffs ---------

# Agent 1: Order status agent - Default handoffs used here
order_status_agent: Agent = Agent(
    name="Order Status Agent",
    instructions="You are an agent who can check the status of customer orders and provide updates.",
)

# Agent 2: Refund agent - Customized handoff used here
refund_agent: Agent = Agent(
    name="Refund Agent",
    instructions="You are an agent who can assist with processing refunds and handling related inquiries.",
)

class RefundData(BaseModel):
    order_id: str
    reason: str

def on_handoff(agent_context: RunContextWrapper[None], input_data: RefundData):
    print(f"[{datetime.datetime.now()}] Refund handoff occurred with order ID: {input_data.order_id} and reason: {input_data.reason}")

customized_refund_agent_handoff = handoff(
    agent=refund_agent,
    tool_name_override="refund_request_handler",
    tool_description_override="Handles refund and return requests in detail.",
    on_handoff=on_handoff,
    input_type=RefundData
)

# Agent 3: Escalation agent
escalation_agent: Agent = Agent(
    name="Escalation Agent",
    instructions="You are an agent who can handle escalated customer issues and provide advanced support.",
)

class EscalationData(BaseModel):
    reason: str

def on_escalation_handoff(agent_context: RunContextWrapper[None], input_data: EscalationData):
    print(f"[{datetime.datetime.now()}] Escalation handoff occurred with reason: {input_data.reason}")

customized_escalation_agent_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_escalation_handoff,
    input_type=EscalationData
)

# Agent 4: FAQ Agent
faq_agent: Agent = Agent(
    name="FAQ Agent",
    instructions="You are an agent who can answer frequently asked questions e.g. What is your return policy?, How can I change my email? etc.",
)

customized_faq_agent_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)

#--------- Define Main Agent --------

customer_support_agent: Agent = Agent(
    name="Customer Support Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a customer support agent who can assist with customer inquiries 
and provide solutions to common issues. If the request does not match any known category, 
politely ask the user to rephrase or clarify their question. Then delegate to the appropriate specialized agent if needed.""",
    handoffs=[order_status_agent, customized_refund_agent_handoff, customized_escalation_agent_handoff, customized_faq_agent_handoff]
)

# ------------- Run the Customer Support Agent --------------

async def main():
    tasks = [
        # "My order #12345 hasn't arrived.",
        # "I want to return a defective product.",
        "What is your return policy?",
        # "I am not satisfied with your support. Escalate this!",
        # "Hey! Just checking if you’re open on Sundays?"  # Unknown intent to test fallback
    ]

    for i, task in enumerate(tasks, start=1):
        print(f"\n====== Task {i}: {task} ======")
        result = await Runner.run(customer_support_agent, task)
        print(f"Response: {result.final_output}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
