from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/reviews")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.Reviews).all()

@app.get("/userreview")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.UserReview).all()


