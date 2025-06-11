from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem, InputGuardrailTripwireTriggered, enable_verbose_stdout_logging 
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

instructions=(
    "Check if the user is asking *any kind of math-related question*, "
    "whether it's solving a problem or explaining a math concept. "
    "Return `is_math_homework=True` if the input is likely related to mathematics in an educational or homework context."
)

# Make a guardrail agent that checks if the input is math homework
guardrail_agent = Agent(
    name="Math Homework Guardrail Agent",
    instructions=instructions,
    output_type=MathHomeWorkOutput
)

# Define a guardrail function that product guardrail Function Output
@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:

    print("========running guardrail agent =========")
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=input,
        context=ctx.context
    )

    print("=== Guardrail Output ===")
    print("is_math_homework:", result.final_output.is_math_homework)
    print("reasoning:", result.final_output.reasoning)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework
    )

# ============================ Usage Example ============================ #

# Define a customer support agent
customer_support_agent = Agent(
    name="customer_support_agent",
    instructions="You are a customer support agent. Answer the user's questions.",
    input_guardrails=[math_guardrail]
)

async def main():
    try:
        print("========starting from customer support agent =========")
        result = await Runner.run(
            starting_agent=customer_support_agent,
            input="what is functions in math?"
        )
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")
        # print("Reason:", e.guardrail_output.output_info.reasoning)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
