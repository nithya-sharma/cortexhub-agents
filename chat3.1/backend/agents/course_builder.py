# coursebuilder.py
from fastapi import UploadFile
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import Runnable
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.messages import BaseMessage

from langchain_community.document_loaders import PyPDFLoader
from docx import Document as DocxDocument
import os

# LLM & Parser
llm = ChatOllama(model="llama3.2:1b")
parser = StrOutputParser()

# Prompt with memory placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict educational assistant that only answers questions related to the uploaded course content. "
 "Your job is to structure the course into modules, assign durations, suggest formats (video, text, etc), quizzes, assignments, and project ideas. "
 "You will **not** answer any general, off-topic, or personal questions. "
 "If the user asks something unrelated, politely reply: 'I'm here only to help structure and enhance the course content provided.'"),
    ("placeholder", "{history}"),
    ("user", "{input}")
])

# Core runnable chain
chain: Runnable = prompt | llm | parser

# Session store for memory
store: dict[str, ChatMessageHistory] = {}

def get_memory(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Chain with session-based memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history"
)

# Main handler method
async def build_course(file: UploadFile, session_id: str = "default") -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    content = ""

    try:
        # Parse uploaded file
        if ext == ".pdf":
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            content = "\n".join([p.page_content for p in PyPDFLoader(temp_path).load()])
            os.remove(temp_path)

        elif ext == ".docx":
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            doc = DocxDocument(temp_path)
            content = "\n".join([p.text for p in doc.paragraphs])
            os.remove(temp_path)

        elif ext == ".txt":
            content = (await file.read()).decode("utf-8")

        else:
            return "❌ Unsupported file type."

        # Prompt construction
        prompt_text = f"Create a course structure based on this content:\n\n{content[:2000]}"

        # Invoke with session memory
        response = await chain_with_memory.ainvoke(
            {"input": prompt_text},
            config={"configurable": {"session_id": session_id}}
        )

        # Debug: Print memory
        print("\n🧠 Current Memory for session:", session_id)
        history = get_memory(session_id)
        for msg in history.messages:
            print(f"{msg.type.upper()}: {msg.content}")

        return response

    except Exception as e:
        return f"❌ Failed to process file: {e}"
