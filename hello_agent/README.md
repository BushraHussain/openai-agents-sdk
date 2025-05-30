## Steps to run the OpenAi agents (Agent SDK) using Gemini model as LLM

1. Create a new uv project without --package flag - "uv init project-name"
2. Create a new virtual environement using "uv venv" & activate using "source .venv/bin/activate"
3. Install the dependencies "uv add openai-agents python-dotenv"
4. Create a .env file and add your Gemini key here. GEMINI_API_KEY=...
5. **Synchronous:** Create a file named "synchronous.py" and add the code  to run the agent synchronously using Runner.run_sync(). 
6. To run the synchronous code, Use this command in the terminal - "uv run synchronous.py"
7. **Asynchronou:** Create another file named "asynchronous.py" and add the code to run the agent asynchronously using Runner.run(). 
8. To run the asynchronous code, Use this command in the terminal - "uv run asynchronous.py" 

## Steps to run the OpenAi agents (Agent SDK) using default openAi models as LLM

1. Create a new file named "using_openai_model.py" and add the code.
2. Create a .env file and add OPENAI_API_KEY=... OR in the terminal run export OPENAI_API_KEY=key_here
3. Run the code using the command "uv run using_openai_model.py"

For more details: https://openai.github.io/openai-agents-python/
