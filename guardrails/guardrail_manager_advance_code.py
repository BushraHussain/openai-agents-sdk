from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    InputGuardrailTripwireTriggered,
)
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# =================== Schema ===================

class GuardrailAgentOutput(BaseModel):
    is_flagged: bool
    reasoning: str


# =================== Guardrail Manager ===================

class GuardrailManager:
    def __init__(self, label: str = "default_guardrail"):
        self.label = label
        self.guardrail_agent = self._create_guardrail_agent()

    def _create_guardrail_agent(self) -> Agent:
        instructions = f"""
        You are a guardrail agent responsible for detecting input that should NOT be processed by a customer support agent.
        Flag anything that:
        - Is a math problem
        - Is toxic or harmful
        - Violates policy
        - Is irrelevant to customer support

        Examples:
        If the user says: "solve 2x + 4 = 10", respond:
        {{
            "is_flagged": true,
            "reasoning": "This is a math homework request."
        }}

        If the user says: "Where is my order?", respond:
        {{
            "is_flagged": false,
            "reasoning": "This is a valid customer support question."
        }}
        """
        return Agent(
            name=f"{self.label}_agent",
            instructions=instructions,
            output_type=GuardrailAgentOutput
        )

    @input_guardrail
    async def validate(self, ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
        print(f"\n[{self.label}] Running Guardrail Agent...")
        result = await Runner.run(
            starting_agent=self.guardrail_agent,
            input=input,
            context=ctx.context
        )

        print(f"[{self.label}] Flagged: {result.final_output.is_flagged}")
        print(f"[{self.label}] Reason: {result.final_output.reasoning}\n")

        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=result.final_output.is_flagged
        )


# =================== Customer Support Agent ===================

guardrail_manager = GuardrailManager(label="support_input_guardrail")

customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. Only answer valid, relevant customer support questions.",
    input_guardrails=[guardrail_manager.validate]
)

# =================== Main ===================

async def main():
    try:
        print("\n=== Starting Customer Support Agent ===\n")
        result = await Runner.run(
            starting_agent=customer_support_agent,
            input="Can you help me solve this: 5x - 2 = 18?"
        )
        print(f"Guardrail didn't trip. Final response:\n{result.final_output}")

    except InputGuardrailTripwireTriggered:
        print("Guardrail Tripwire Triggered!")
        # print("Reason:", e.guardrail_output.output_info.reasoning) # Not supported

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
