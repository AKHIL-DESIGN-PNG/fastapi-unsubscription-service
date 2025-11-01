from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from unsubscription_service.database import get_db
from unsubscription_service.models import User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

router = APIRouter(prefix="/subscriptions", tags=["=>Subscription Management"])

def format_user_data(user: User, is_active: bool) -> dict:
    """Helper function to format user data based on subscription status."""
    if is_active:
        return {
            "username": user.username,
            "status": "Active (Subscribed)"
        }
    else:
        return {
            "username": user.username,
            "email": user.email,
            "status": "Inactive (Unsubscribed)",
            "reason": user.reason,
            "comments": user.comments
        }

@router.get("/list", status_code=status.HTTP_200_OK)
async def get_subscriptions(
    is_active: Optional[bool] = Query(None, description="Filter by subscription status: true for subscribed, false for unsubscribed"),
    db: AsyncSession = Depends(get_db)
):
    """
    API to retrieve subscribed, unsubscribed users, or all users based on 'is_active'.
    """
    try:
        # Filter users based on is_active status, if provided
        query = select(User)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        # Log the query to check
        logging.info(f"Executing query: {query}")

        # Ensure the session is properly managed and awaited
        async with db.begin():
            result = await db.execute(query)
            users: List[User] = result.scalars().all()

        # Log the results to see the data fetched
        logging.info(f"Fetched {len(users)} users from the database.")

        if not users:
            detail = "No subscribed users found." if is_active else "No unsubscribed users found."
            logging.warning(detail)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

        # Format user data for both subscribed and unsubscribed users
        subscribed_users = [format_user_data(user, True) for user in users if user.is_active]
        unsubscribed_users = [format_user_data(user, False) for user in users if not user.is_active]

        if is_active is None:
            # Return both subscribed and unsubscribed users if no filter is applied
            return {
                "message": "All users retrieved successfully.",
                "subscribed_users": subscribed_users,
                "unsubscribed_users": unsubscribed_users
            }

        # Return filtered result
        response_data = subscribed_users if is_active else unsubscribed_users
        return {
            "message": f"{'Subscribed' if is_active else 'Unsubscribed'} users retrieved successfully.",
            "data": response_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in /subscriptions/list endpoint: {str(e)}")  # Log the error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
