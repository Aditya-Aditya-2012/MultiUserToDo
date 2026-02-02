from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import text
from app.schemas import UserCreate, UserOut, Token, TokenData, TaskCreate, TaskOut, TaskUpdate
from app.models import User, Task
from app.security import get_hash, create_access_token, verify_password
from app.dependencies import get_current_user
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import uuid
app = FastAPI()

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return{"status": "unhealthy", "error" : {str(e)}} 

@app.post("/signup", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_passowrd = get_hash(user.password)
    new_user = User(
        username = user.username,
        password = hashed_passowrd        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserOut)
def read_users_me(current_user: User=Depends(get_current_user)):
    return current_user

@app.post("/tasks", response_model=TaskOut)
def create_task(
    task: TaskCreate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    new_task = Task(
        taskname = task.taskname,
        is_complete = task.is_complete,
        user_id = current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task
    
@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    task_query = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id)
    task = task_query.first()
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task_query.delete(synchronize_session=False)
    db.commit()
    
    return None

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    task_query = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    
    task=task_query.first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
        
    update_dict = task_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    
    return task
    