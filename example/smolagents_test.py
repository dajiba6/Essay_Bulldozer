# !pip install smolagents[litellm]
from smolagents import CodeAgent, LiteLLMModel
from smolagents import ToolCallingAgent
from smolagents import DuckDuckGoSearchTool


model = LiteLLMModel(
    model_id="ollama_chat/llama3.2",  # This model is a bit weak for agentic behaviours though
    api_base="http://localhost:11434",  # replace with 127.0.0.1:11434 or remote open-ai compatible server if necessary
    api_key="YOUR_API_KEY",  # replace with API key if necessary
    num_ctx=8192,  # ollama default is 2048 which will fail horribly. 8192 works for easy tasks, more is better. Check https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator to calculate how much VRAM this will need for the selected model.
)

# agent = CodeAgent(tools=[], model=model, add_base_tools=True)

# agent.run(
#     "plot a circle in terminal",
# )
prompt = "tell me some thing about the huawei gang"
# agent = CodeAgent(
#     tools=[], model=model, additional_authorized_imports=["requests", "bs4"]
# )
# agent.run(prompt)


search_tool = DuckDuckGoSearchTool()

agent = ToolCallingAgent(tools=[search_tool], model=model)
agent.run(prompt)
