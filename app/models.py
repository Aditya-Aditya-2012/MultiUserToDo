from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base
from typing import List

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False, index=True)
    password = mapped_column(String, nullable=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="owner")
    
class Task(Base):
    __tablename__ = "tasks"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    taskname = mapped_column(String, nullable=False)
    is_complete = mapped_column(Boolean, default=False)
    owner: Mapped["User"] = relationship(back_populates="tasks")
    
    
"""ondelete="CASCADE": This is a huge system design concept. 
It means if a user is deleted, their tasks are automatically deleted by the database. 
Without this, your database would have "orphaned" tasks that belong to nobody."""