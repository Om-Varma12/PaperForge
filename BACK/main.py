# back/main.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from utils.prompt import prompt_generator
from services.llm import sendRequest
from services.ieeeFormat import generate_ieee_paper
import json
import asyncio

app = FastAPI()


class Schema(BaseModel):
    overview: str = Field(..., min_length=30)
    format: str
    npages: int


def create_sse_message(stage: str, status: str, data: dict = None):
    """Create a Server-Sent Event message"""
    message = {
        "stage": stage,
        "status": status,
        "data": data or {}
    }
    return f"data: {json.dumps(message)}\n\n"


async def generate_paper_stream(data: Schema):
    """Generator function that yields status updates"""
    
    try:
        # Stage 1: Validation
        yield create_sse_message("validation", "started")
        await asyncio.sleep(0.5)  # Simulate validation time
        
        if len(data.overview.strip()) < 30:
            yield create_sse_message("validation", "error", 
                                    {"message": "Overview too short"})
            return
        
        yield create_sse_message("validation", "completed")
        
        # Stage 2: Prompt Generation
        yield create_sse_message("prompt_generation", "started")
        prompt_result = prompt_generator(data.overview)
        
        if prompt_result["status"] != "done":
            yield create_sse_message("prompt_generation", "error",
                                    {"message": "Failed to generate prompt"})
            return
        
        yield create_sse_message("prompt_generation", "completed")
        
        # Stage 3: LLM Response
        yield create_sse_message("llm_response", "started")
        llm_response = sendRequest(prompt_result["prompt"])
        yield create_sse_message("llm_response", "completed")
        
        # Stage 4: Document Generation
        yield create_sse_message("document_generation", "started")
        output_file = generate_ieee_paper(llm_response)
        yield create_sse_message("document_generation", "completed")
        
        # Final success message
        yield create_sse_message("complete", "success", 
                                {"file": output_file})
        
    except Exception as e:
        yield create_sse_message("error", "failed",
                                {"message": str(e)})


@app.post("/generate-docs-stream")
async def generate_docs_stream(data: Schema):
    """Streaming endpoint that sends real-time status updates"""
    return StreamingResponse(
        generate_paper_stream(data),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/generate-docs")
async def generate_docs(data: Schema):
    """Original non-streaming endpoint (kept for backwards compatibility)"""
    prompt_result = prompt_generator(data.overview)
    if prompt_result["status"] != "done":
        return {"status": "error"}

    llm_response = sendRequest(prompt_result["prompt"])
    output_file = generate_ieee_paper(llm_response)

    return {
        "status": "success",
        "file": output_file
    }