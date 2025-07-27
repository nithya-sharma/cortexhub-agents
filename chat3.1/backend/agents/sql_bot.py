# sqlbotpy
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory

# Model and parser
llm = ChatOllama(model="gemma3:12b")
parser = StrOutputParser()

# Prompt template with session memory
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a SQL-only assistant. "
     "You MUST ONLY answer questions related to SQL. "
     "For ANY question NOT about SQL, respond exactly with: "
     "'Sorry, I can only help with SQL-related queries.'"),
    ("placeholder", "{history}"),  # inject memory here
    ("user", "{input}")
])

# Chain
chain: Runnable = prompt | llm | parser

# Memory store
store: dict[str, ChatMessageHistory] = {}

def get_memory(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history"
)

# Main method to expose
async def answer_sql(prompt: str, session_id: str = "default") -> str:
    try:
        response = await chain_with_memory.ainvoke(
            {"input": prompt},
            config={"configurable": {"session_id": session_id}}
        )

        # Debug: Print memory
        print("\n🧠 Current Memory:")
        history = get_memory(session_id)
        for msg in history.messages:
            print(f"{msg.type.upper()}: {msg.content}")

        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"
