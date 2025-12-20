from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from services.formatter import format_document
from services.llm import sendRequest
from services.fileCreator import create_document

app = FastAPI()

class Schema(BaseModel):
    overview: str = Field(
        ...,
        min_length=30,
        description="Project overview must be at least 30 characters long"
    )
    format: str
    npages: int
    section: list[str] = Field(
        ...,
        min_items=5,
        description="Select at least 5 paper sections"
    )

@app.post("/generate-docs")
async def generate_docs(data: Schema):
    #start validation spinner
    result = format_document(data.overview, data.npages, data.section)
    # stop validation spinner and start formating content spinner
    
    if result.get('status') == 'done':
        #stop formating content spinner and start LLM request spinner
        llmResponse = sendRequest(result.get('prompt'))
        # stop LLM request spinner and start docs creating spinner
        
        create_document(llmResponse, data.format)
        
    else:
        return {
            "status": "error",
            "message": "Prompt generation failed"
        }
    
    return {
        "status": "success",
    }