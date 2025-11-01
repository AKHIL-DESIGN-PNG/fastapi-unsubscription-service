from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer  

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users_details"  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    reason: Mapped[str] = mapped_column(String(100), nullable=False)
    comments: Mapped[str] = mapped_column(String(255), nullable=True)
