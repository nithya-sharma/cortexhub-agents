# generalchat assistant
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory

# Model
llm = ChatOllama(model="llama3.2:1b")
parser = StrOutputParser()

# Prompt
prompt = ChatPromptTemplate.from_messages([
    # ("system", 
    #  "You are a helpful assistant. "),
    ("system", "You an CortexHub AI, a helpful assistant created by BetaMONKS. "
    "Your job is to help users by answering questions, assisting with tasks, and engaging in productive conversation. "
    "Be honest, precise, safe, and follow the user's instructions as closely as possible. "
    "If the user asks something unclear, ask clarifying questions."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# Core chain
chain: Runnable = prompt | llm | parser

# Session store
store: dict[str, ChatMessageHistory] = {}

def get_memory(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Add memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history"
)

# Final exposed method
async def chat_response(prompt: str, session_id: str = "default") -> str:
    try:
        response = await chain_with_memory.ainvoke(
            {"input": prompt},
            config={"configurable": {"session_id": session_id}}
        )

        # Print memory
        print("\n🧠 Current Memory:")
        history = get_memory(session_id)
        for msg in history.messages:
            print(f"{msg.type.upper()}: {msg.content}")

        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"