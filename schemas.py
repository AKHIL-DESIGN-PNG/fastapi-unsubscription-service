from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UnsubscribeRequest(BaseModel):
    username: str = Field(..., title="Username of the user", example="john_doe")
    email: EmailStr = Field(..., title="User's email", example="john.doe@example.com")  # Added email with validation
    reason: str = Field(..., title="Reason for unsubscription", example="Other")
    comments: Optional[str] = Field(None, title="Additional comments")

    # Removed Pydantic validator to avoid 422 errors; validation moved to route handler
