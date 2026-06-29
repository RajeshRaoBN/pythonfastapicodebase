# 1. Initialize a structured, modern Python project
uv init my-fastapi-app
cd my-fastapi-app

# 2. Add FastAPI as a managed dependency
uv add "fastapi[standard]"

uv run fastapi dev main.py

pip freeze > requirement.txt