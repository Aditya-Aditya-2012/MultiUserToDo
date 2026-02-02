# define the user models for user creation and log output
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserOut(BaseModel):
    id: int
    username: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None=None
    
class TaskCreate(BaseModel):
    taskname: str
    is_complete: Optional[bool] = False

class TaskOut(BaseModel):
    id: int
    taskname: str
    is_complete: bool
    user_id: int
    
    class Config:
        from_attributes = True
        
class TaskUpdate(BaseModel):
    taskname: Optional[str] = None
    is_complete: Optional[bool] = None
    
