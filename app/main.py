from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text

app = FastAPI()

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return{"status": "unhealthy", "error" : {str(e)}} 
