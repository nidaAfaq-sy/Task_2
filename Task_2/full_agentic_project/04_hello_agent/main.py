from agents import Agent, OpenAIChatCompletionsModel,AsyncOpenAI, Runner, set_tracing_disabled
from dotenv import load_dotenv
import os
import chainlit as cl

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3-0324:free"

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

set_tracing_disabled(disabled=True)


# This agent will use the custom LLM provider
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant to answer any question.",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! How can I help you today?").send()

   
@cl.on_message
async def handle_message(message:cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(
        starting_agent=agent,
        input=history
    )
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()



