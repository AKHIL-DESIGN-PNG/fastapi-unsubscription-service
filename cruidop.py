from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from database import get_db
from sqlalchemy import select  
router = APIRouter()
@router.get("/users_details")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    
    return result.scalars().all()


