from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://adityamac@localhost:5432/tododb" #Driver agnostic URL 

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False ,bind=engine) #Keep autocommit = false

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        
