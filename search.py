from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy import select
from unsubscription_service.database import get_db
from unsubscription_service.models import User
from typing import List

router = APIRouter(prefix="/search", tags=["=>Search and Filter"])

@router.get("/subscriptions", status_code=status.HTTP_200_OK)
async def search_subscriptions(
    username: str | None = Query(None, description="Filter by username"),
    email: str | None = Query(None, description="Filter by email"),
    reason: str | None = Query(None, description="Filter by reason"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(User)

        if username:
            query = query.where(func.lower(User.username).ilike(f"%{username.lower()}%"))
        if email:
            query = query.where(func.lower(User.email).ilike(f"%{email.lower()}%"))
        if reason:
            query = query.where(func.lower(User.reason).ilike(f"%{reason.lower()}%"))

        result = await db.execute(query)
        users: List[User] = result.scalars().all()

        formatted_users = [
            {
                "username": user.username,
                "email": user.email,
                "reason": user.reason,
                "comments": user.comments,
                "is_active": user.is_active
            } for user in users
        ]

        if not formatted_users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No matching subscription details found."
            )

        return {
            "status_code": status.HTTP_200_OK,
            "message": "Search results retrieved successfully.",
            "data": formatted_users
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred."
        )
