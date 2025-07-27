# ├── backend/main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.course_builder import build_course
from agents.sql_bot import answer_sql
from agents.image_analyser import image_analyzer
from agents.general_chat import chat_response

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptInput(BaseModel):
    prompt: str
    session_id: str = "default"

@app.post("/general_chat/")
async def general_chat_route(data: PromptInput):
    result = await chat_response(data.prompt, data.session_id)
    return {"output": result}

@app.post("/course_builder/")
async def course_builder_route(file: UploadFile = File(...)):
    result = await build_course(file)
    return {"output": result}

@app.post("/sql_bot/")
async def sql_bot_route(data: PromptInput):
    result = await answer_sql(data.prompt)
    return {"output": result}

@app.post("/image_analyzer/")
async def image_analyzer_route(file: UploadFile = File(...)):
    result = await image_analyzer(file)
    return {"output": result}
    # return result