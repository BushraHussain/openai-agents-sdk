from agents import Agent, Runner, GuardrailFunctionOutput, input_guardrail, RunContextWrapper, TResponseInputItem, InputGuardrailTripwireTriggered, enable_verbose_stdout_logging
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

# ================ Guardrail Agent ==================

class GuardrailAgentOutput(BaseModel):
    is_flagged:bool
    reasoning:str

instructions = """
You are a guardrail agent that must only respond with structured JSON in the format:
{
  "is_flagged": true or false,
  "reasoning": "a short explanation"
}

Your job is to determine if the user input is irrelevant, toxic, or violates any policy.
Respond ONLY in the above JSON format. Do NOT add anything else.
"""

# instructions = """
#     You are a guardrail agent that check user input if it contains any irrelevant thing that is not relevant to customer support. 
#     Any toxic or harmful content should be flagged.
#     And policy violations should be flagged.

#     Means if a user input is not relevant to the customer support agent,
#     return `is_flagged=True` and provide a reasoning for why the input is not relevant.

#     If the user says: "solve 2x + 4 = 10", respond:
#     {
#     "is_flagged": True,
#     "reasoning": "This is a math homework request."
#     }

#     If the user says: "Where is my order?", respond:
#     {
#     "is_flagged": False,
#     "reasoning": "This is a valid customer support question."
#     }
#     """

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions=instructions,
    output_type=GuardrailAgentOutput
)

# Define a guardrail function
@input_guardrail
async def guardrail_function(
    ctx:RunContextWrapper[None], 
    agent:Agent,
    input:str | list[TResponseInputItem]
)-> GuardrailFunctionOutput:
    
    # print(f"Input to guardrail agent: {input}")
    # print(f"Context: {ctx.context}")
    # print(f"Agent: {agent.name}")

    print("========Running guardrail agent =========")

    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=input,
        context=ctx.context
    )

    print(f"Result of guardrail agent: {result.final_output}")

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_flagged
    )


# ==================== Customer Support Agent ==================== #

customer_support_agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. Answer only if the user's questions if it is relevant to customer support",
    input_guardrails=[guardrail_function]
)

async def main():
    try:
        print("========Starting from customer support agent =========")
        result = await Runner.run(
            starting_agent=customer_support_agent,
            input="I want to know about my order status"
        )
        print(f"Guardrail didn't trip - this is expected. Result: {result.final_output}")

    except InputGuardrailTripwireTriggered:
        print("Guardrail tripwire triggered..")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())














