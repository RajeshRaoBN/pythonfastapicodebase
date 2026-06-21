import os
import io
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Google GenAI Backend",
    description="Production-ready FastAPI app powered by the Google GenAI SDK.",
    version="1.0.0",
)

# Initialize the official Google GenAI Client
# The SDK automatically uses os.environ["GEMINI_API_KEY"] if not passed explicitly
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY missing from environment variables.")

client = genai.Client(api_key=api_key)


# Define a standard Pydantic schema for text generation requests
class PromptRequest(BaseModel):
    prompt: str = Field(
        ..., min_length=1, description="The prompt text to send to Gemini."
    )
    model_name: str = Field(
        "gemini-2.5-flash", description="The specific Gemini model to target."
    )


@app.get("/")
def read_root():
    """
    Health check endpoint to ensure server functionality.
    """
    return {"status": "online", "framework": "FastAPI", "engine": "Google GenAI SDK"}
