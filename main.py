from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas
from typing import List

app = FastAPI()

# --- USERS ---
@app.get("/users/", response_model=List[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Fetches auto-generated id and created_at
    return db_user

# --- REVIEWS ---
@app.get("/reviews/", response_model=List[schemas.ReviewsResponse])
def read_reviews(db: Session = Depends(get_db)):
    return db.query(models.Reviews).all()

@app.post("/reviews/", response_model=schemas.ReviewsResponse)
def create_review(review: schemas.ReviewsCreate, db: Session = Depends(get_db)):
    db_review = models.Reviews(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# --- USER-REVIEWS ---
# Add this to main.py to allow browser viewing
@app.get("/user-reviews/", response_model=List[schemas.UserReviewResponse])
def get_user_reviews(db: Session = Depends(get_db)):
    return db.query(models.UserReview).all()


@app.post("/user-reviews/", response_model=schemas.UserReviewResponse)
def link_review(link: schemas.UserReviewCreate, db: Session = Depends(get_db)):
    db_link = models.UserReview(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link