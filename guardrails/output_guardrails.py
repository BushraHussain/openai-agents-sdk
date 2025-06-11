from agents import Agent, Runner, GuardrailFunctionOutput, output_guardrail, RunContextWrapper, TResponseInputItem, OutputGuardrailTripwireTriggered, enable_verbose_stdout_logging
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

# ================ Output Guardrail Agent ==================

class CustomerAgentOutput(BaseModel): 
    response: str

class GuardrailAgentOutput(BaseModel):
    is_math:bool
    reasoning:str

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="""
    You are a guardrail agent that checks agent's output for mathematical content and
    must only respond with structured JSON in the format:
    {
      "is_math": true or false,
      "reasoning": "a short explanation"
    }
    Your job is to determine if the agent output contains mathematical content.
    Respond ONLY in the above JSON format. Do NOT add anything else.
    """,
    output_type=GuardrailAgentOutput
)

# Define a guardrail function
@output_guardrail
async def guardrail_function(
        ctx:RunContextWrapper[None],
        agent:Agent,
        output:CustomerAgentOutput
)->GuardrailFunctionOutput:
    
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=output.response,
        context=ctx.context
    )

    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered= result.final_output.is_math,
    )


# ================ define a customer support agent ==================

customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions=""",
    You are a customer support agent that helps users with their queries only related to customer support.
    """,
    output_guardrails=[guardrail_function],
    output_type=CustomerAgentOutput
)

async def main():
    try:
        await Runner.run(
            starting_agent=customer_support_agent,
            input="Hello, can you help me solve for x: 2x + 3 = 11?"
        )

        print("Tripwire didn't trigger - unexpected")

    except OutputGuardrailTripwireTriggered:
        print("Tripwire triggered - output contained mathematical content")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())