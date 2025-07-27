import base64
from fastapi import UploadFile
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory

# Model: Multimodal Vision Model
llm = ChatOllama(model="llama3.2-vision:11b")
parser = StrOutputParser()

# Prompt Template with memory support
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an image analysis expert. Analyze uploaded images and explain what they contain in clear and accurate terms."),
    ("placeholder", "{history}"),
    ("user", "{input}")
])

# Runnable chain
chain: Runnable = prompt | llm | parser

# In-memory chat session store
store: dict[str, ChatMessageHistory] = {}

def get_memory(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Chain with memory support
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history"
)

# Final function to invoke the vision model
async def image_analyzer(file: UploadFile, session_id: str = "default") -> str:
    try:
        image_data = await file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        mime_type = file.content_type
        image_with_prefix = f"data:{mime_type};base64,{encoded_image}"

        # Compose message and input string
        visual_msg = HumanMessage(
            content=[
                {"type": "text", "text": "Analyze this image and explain what is seen."},
                {"type": "image_url", "image_url": {"url": image_with_prefix}}
            ]
        )

        # Append the image instruction to history and ask a follow-up input to store in memory
        response = await chain_with_memory.ainvoke(
            {"input": "Please analyze the uploaded image."},
            config={"configurable": {"session_id": session_id}, "messages": [visual_msg]}
        )

        # 🧠 Print memory to console
        print(f"\n🧠 Current Memory for session '{session_id}':")
        history = get_memory(session_id)
        for msg in history.messages:
            print(f"{msg.type.upper()}: {msg.content}")

        return response

    except Exception as e:
        return f"❌ Image analysis failed: {e}"
