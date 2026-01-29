import os
from google import genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/generate")
async def generate_text(request: PromptRequest):

    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured")

    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=request.prompt
        )

        return {"response": response.text}

    except Exception as e:
        print(f"Error details: {e}")
        raise HTTPException(status_code=500, detail=str(e))
