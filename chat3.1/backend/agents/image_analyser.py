# image_analyzer.py
import base64
from fastapi import UploadFile
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# llm = ChatOllama(model="llama3.2-vision:11b")
llm = ChatOllama(model="gemma3:4b")

async def image_analyzer(file: UploadFile) -> str:
    try:
        image_data = await file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        mime_type = file.content_type
        image_with_prefix = f"data:{mime_type};base64,{encoded_image}"

        message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": (
                "extract the name , dob, address, gender, type of govt id, id no, andgive it in json format"
            )
        },
        {
            "type": "image_url",
            "image_url": {"url": image_with_prefix}
        }
    ]
)

        # return llm.invoke([message])
        result = llm.invoke([message])
        return result.content
    except Exception as e:
        return f"❌ Image analysis failed: {e}"

# import base64
# from fastapi import UploadFile
# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.runnables import Runnable
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import HumanMessage
# from langchain_community.chat_message_histories.in_memory import ChatMessageHistory

# # Model: Multimodal Vision Model
# llm = ChatOllama(model="llama3.2-vision:11b")
# parser = StrOutputParser()

# # Prompt Template with memory support
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an image analysis expert. Analyze uploaded images and explain what they contain in clear and accurate terms."),
#     ("placeholder", "{history}"),
#     ("user", "{input}")
# ])

# # Runnable chain
# chain: Runnable = prompt | llm | parser

# # In-memory chat session store
# store: dict[str, ChatMessageHistory] = {}

# def get_memory(session_id: str) -> ChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]

# # Chain with memory support
# chain_with_memory = RunnableWithMessageHistory(
#     chain,
#     get_memory,
#     input_messages_key="input",
#     history_messages_key="history"
# )

# # Final function to invoke the vision model
# async def image_analyzer(file: UploadFile, session_id: str = "default") -> str:
#     try:
#         image_data = await file.read()
#         encoded_image = base64.b64encode(image_data).decode("utf-8")
#         mime_type = file.content_type
#         image_with_prefix = f"data:{mime_type};base64,{encoded_image}"

#         # Compose message and input string
#         visual_msg = HumanMessage(
#             content=[
#                 {"type": "text", "text": "Analyze this image and explain what is seen."},
#                 {"type": "image_url", "image_url": {"url": image_with_prefix}}
#             ]
#         )

#         # Append the image instruction to history and ask a follow-up input to store in memory
#         response = await chain_with_memory.ainvoke(
#             {"input": "Please analyze the uploaded image."},
#             config={"configurable": {"session_id": session_id}, "messages": [visual_msg]}
#         )

#         # 🧠 Print memory to console
#         print(f"\n🧠 Current Memory for session '{session_id}':")
#         history = get_memory(session_id)
#         for msg in history.messages:
#             print(f"{msg.type.upper()}: {msg.content}")

#         return response

#     except Exception as e:
#         return f"❌ Image analysis failed: {e}"


# # # agents/image_analyser.py
# # from fastapi import UploadFile
# # from langchain_ollama import ChatOllama
# # from langchain_core.messages import HumanMessage
# # import base64

# # llm = ChatOllama(model="llama3.2-vision:11b")

# # async def image_analyzer(file: UploadFile):
# #     try:
# #         content = await file.read()
# #         mime = file.content_type or "image/png"
# #         encoded = base64.b64encode(content).decode('utf-8')
# #         data_url = f"data:{mime};base64,{encoded}"  # Or just use `encoded` if model expects raw base64

# #         prompt = "What do you see in this image? Analyse and give insights."
# #         response = llm.invoke([
# #             HumanMessage(content=[
# #                 {"type": "image_url", "image_url": {"url": data_url}},
# #                 {"type": "text", "text": prompt}
# #             ])
# #         ])
# #         return response.content
# #     except Exception as e:
# #         return {"output": f"Error analyzing image: {str(e)}"}

# import base64
# from fastapi import UploadFile
# from langchain_ollama import ChatOllama
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.runnables import Runnable
# from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate

# # 🔹 Vision model
# llm = ChatOllama(model="llama3.2-vision:11b")
# parser = StrOutputParser()

# # 🔹 Prompt: A generic system prompt with memory placeholder
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an image analysis assistant. Describe the image and provide helpful context."),
#     ("placeholder", "{history}"),
#     ("human", "{input}")
# ])

# # 🔹 Chain
# chain: Runnable = prompt | llm | parser

# # 🔹 In-memory session store
# store: dict[str, ChatMessageHistory] = {}

# def get_memory(session_id: str) -> ChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]

# # 🔹 Chain with memory
# chain_with_memory = RunnableWithMessageHistory(
#     chain,
#     get_memory,
#     input_messages_key="input",
#     history_messages_key="history"
# )

# # 🔹 Main function
# async def image_analyzer(file: UploadFile, session_id: str = "default") -> str:
#     try:
#         image_data = await file.read()
#         encoded_image = base64.b64encode(image_data).decode("utf-8")
#         mime_type = file.content_type
#         image_with_prefix = f"data:{mime_type};base64,{encoded_image}"

#         # 🗨️ Prompt text
#         prompt_text = "Analyze this image and explain what is seen."

#         # Use HumanMessage content with image_url
#         human_msg = HumanMessage(content=[
#             {"type": "text", "text": prompt_text},
#             {"type": "image_url", "image_url": {"url": image_with_prefix}}
#         ])

#         # Send it directly to the LLM
#         response = await chain_with_memory.ainvoke(
#             {"input": human_msg},
#             config={"configurable": {"session_id": session_id}}
#         )

#         # Optional: Print history
#         history = get_memory(session_id)
#         for msg in history.messages:
#             print(f"{msg.type.upper()}: {msg.content}")

#         return response
#     except Exception as e:
#         return f"❌ Image analysis failed: {e}"
