## Steps to run the OpenAi agents (Agent SDK) using Gemini model as LLM

1. Create a new uv project without --package flag - "uv init project-name"
2. Create a new virtual environement using "uv venv" & activate using "source .venv/bin/activate"
3. Install the dependencies "uv add openai-agents python-dotenv"
4. *Synchronous running:* Create a file named "synchronous.py" and add the code  to run the agent synchronously using Runner.run_sync(). 
5. To run the synchronous code, Use this command in the terminal - "uv run synchronous.py"
6. *Asynchronous running:* Create another file named "asynchronous.py" and add the code to run the agent asynchronously using Runner.run(). 
7. To run the asynchronous code, Use this command in the terminal - "uv run asynchronous.py" 

For more details: https://openai.github.io/openai-agents-python/
