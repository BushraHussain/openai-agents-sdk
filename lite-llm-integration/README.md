## Setup Instructions

1. Install LiteLLM with OpenAI Agents support

- Run the following command to install the required dependencies:

```bash
uv add "openai-agents[litellm]"
```

2. Verify LiteLLM Integration
- Ensure LiteLLM is correctly integrated by reviewing the file: litellm_integration.py

3. Use Multiple Models at the Agent Level

- Refer to mix_match_models.py to see how to assign different models to individual agents. 
- Example configuration:
    - Guardrail Agent — uses the Gemini model
    - Main Agent — uses the OpenAI model