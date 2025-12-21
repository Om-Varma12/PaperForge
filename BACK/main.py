# main.py

from fastapi import FastAPI
from pydantic import BaseModel, Field
from utils.prompt import prompt_generator
from services.llm import sendRequest
from services.ieeeFormat import generate_ieee_paper

app = FastAPI()

class Schema(BaseModel):
    overview: str = Field(..., min_length=30)
    format: str
    npages: int


@app.post("/generate-docs")
async def generate_docs(data: Schema):
    # 1️⃣ Prompt generation
    prompt_result = prompt_generator(data.overview)

    if prompt_result.get("status") != "done":
        return {"status": "error", "message": "Prompt generation failed"}

    # 2️⃣ LLM call
    llm_response = sendRequest(prompt_result["prompt"])

    # 3️⃣ DOCX generation
    output_file = generate_ieee_paper(llm_response)

    return {
        "status": "success",
        "file": output_file
    }
