# 

import sys
sys.path.append("C:/CodeTru")
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from unsubscription_service.models import User
from unsubscription_service.database import get_db
import logging

# Initialize logging for debugging and error tracking
logging.basicConfig(level=logging.INFO)

# Router for Owner's View
view_router = APIRouter(prefix="/unsubscriptions", tags=["=>Owner_view."])

@view_router.get("/owner_view", status_code=status.HTTP_200_OK)
async def get_unsubscriptions(
    username: str = Query(None, description="Filter by username"),
    email: str = Query(None, description="Filter by email"),
    reason: str = Query(None, description="Filter by reason"),
    db: AsyncSession = Depends(get_db)
):
    """
    API for Owner's View to retrieve unsubscribed user details based on filters.
    Filters can include username, email, or reason.
    """
    try:
        # Build filters dynamically
        filters = []
        if username:
            filters.append(func.lower(User.username) == username.lower())
        if email:
            filters.append(func.lower(User.email) == email.lower())
        if reason:
            filters.append(func.lower(User.reason) == reason.lower())

        query = select(User).where(*filters)

        # Logging the query filters
        logging.info(f"Executing query with filters: {filters}")

        try:
            result = await db.execute(query)
            users = result.scalars().all()
        except Exception as db_exc:
            logging.error(f"Database execution error: {str(db_exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database execution error occurred"
            )

        # Handle "no results found" case
        if not users:
            logging.info("No matching unsubscriptions found for the provided filters.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No matching unsubscriptions found..."
            )

        # Prepare response data
        response_data = [
            {
                "username": user.username,
                "email": user.email,
                "reason": user.reason,
                "comments": user.comments
            }
            for user in users
        ]

        logging.info(f"Unsubscriptions retrieved successfully: {response_data}")

        return {
            "message": "Unsubscriptions retrieved successfully.",
            "data": response_data
        }

    except HTTPException as http_exc:
        # Handle HTTP-specific exceptions
        raise http_exc

    except Exception as e:
        # Catch unexpected errors
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred"
        )
