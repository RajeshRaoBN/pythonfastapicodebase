# Create and navigate to the project directory
mkdir fastapi-genai-app
cd fastapi-genai-app

# Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install FastAPI, Uvicorn, and the new Google GenAI SDK
pip install fastapi uvicorn google-genai pydantic python-dotenv Pillow
