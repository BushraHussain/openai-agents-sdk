from openai import AsyncOpenAI
from agents import Agent, Runner, GuardrailFunctionOutput, input_guardrail, RunContextWrapper, TResponseInputItem, InputGuardrailTripwireTriggered, enable_verbose_stdout_logging, OpenAIChatCompletionsModel
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
enable_verbose_stdout_logging()

gemini_key = os.getenv("GEMINI_API_KEY")
base_url ="https://generativelanguage.googleapis.com/v1beta/openai/"

client = AsyncOpenAI(
    base_url=base_url,
    api_key=gemini_key
)

class GuardrailAgentOutput(BaseModel):
    is_flagged:bool
    reason:str

# Gemini model for guardrail agent
guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="You are a guardrail agent that checks user input if it contains bad language",
    output_type=GuardrailAgentOutput,
    model = LitellmModel(model="gemini/gemini-1.5-flash", api_key=gemini_key)
)

@input_guardrail
async def guardrail_function(
    ctx:RunContextWrapper[None],
    agent:Agent,
    input:str | TResponseInputItem
):
    
    print("==============Guardrail Agent is running===================")

    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=input,
        context= ctx.context
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_flagged
    )


async def main():

    try:
        # Openai gpt-4o model for guardrail agent
        math_agent = Agent(
            name="math agent",
            instructions="You're a math agent that assist users in math problems",
            input_guardrails=[guardrail_function],
            model= "gpt-4o"
        )

        print("==============Math Agent is running===================")

        await Runner.run(
            starting_agent=math_agent,
            input="what is 2+3?"
        )

        print("Tripwire didn't trigger")
    
    except InputGuardrailTripwireTriggered:
        print("Tripwire triggered! ")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())