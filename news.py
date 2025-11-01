from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Dummy database of users
users_db = [
    {"id": 1, "username": "john_doe", "email": "john@example.com", "subscribed": True},
    {"id": 2, "username": "jane_smith", "email": "jane@example.com", "subscribed": True}
]

class UnsubscribeRequest(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    reason: Optional[str] = None
    comments: Optional[str] = None

@app.post("/unsubscribe")
def unsubscribe_user(request: UnsubscribeRequest):
    # Ensure at least one identifier is provided
    if not any([request.id, request.username, request.email]):
        raise HTTPException(status_code=400, detail="Provide at least one identifier: id, username, or email.")
    
    # Validate 'comments' if reason is 'Other'
    if request.reason == "Other" and not request.comments:
        raise HTTPException(status_code=400, detail="Comments are required when reason is 'Other'.")

    # Search for user based on given identifier(s)
    user = next((
        u for u in users_db if
        (request.id is not None and u["id"] == request.id) or
        (request.username is not None and u["username"] == request.username) or
        (request.email is not None and u["email"] == request.email)
    ), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Mark user as unsubscribed
    user["subscribed"] = False

    return {"status": 200, "message": "Unsubscribed successfully."}
