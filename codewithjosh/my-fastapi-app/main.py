from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

users = {
    1: {"name": "Alice", "age": 30, "city": "New York", "role": "admin"},
    2: {"name": "Bob", "age": 25, "city": "Los Angeles", "role": "user"},
    3: {"name": "Charlie", "age": 35, "city": "Chicago", "role": "user"},
}

class User(BaseModel):
    name: str
    age: int
    city: str
    role: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    role: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., title="The ID of the user to get", ge=1)):
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users[user_id]

@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_user(user_id: int = Path(..., title="The ID of the user to create", ge=1), user: User = None):
    if user_id in users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data")
    users[user_id] = user.dict()
    return users[user_id]

@app.put("/users/{user_id}")
async def update_user(user_id: int = Path(..., title="The ID of the user to update", ge=1), user_update: UserUpdate = None):
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user update data")
    users[user_id].update(user_update.dict())
    return users[user_id]

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int = Path(..., title="The ID of the user to delete", ge=1)):
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del users[user_id]
    return

@app.get("/users/search/")
async def search_by_name(name: Optional[str] = None):
    if not name:
        return {"message": "Please provide a name to search for."}
    results = []
    for user_id, user in users.items():
        if name is None or name.lower() in user["name"].lower():
            results.append(user)
            if not results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found with the given name")             
    return results