from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from sqlalchemy import desc
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
   # --- 1. PRE-CHECKS FOR UNIQUENESS ---
    
    # Check Email
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered and exists in our database .")

    # Check Personal Website
    if user.personal_website and db.query(models.User).filter(models.User.personal_website == user.personal_website).first():
        raise HTTPException(status_code=400, detail="This personal website URL already exists.")

    # Check Instagram
    if user.instagram_profile and db.query(models.User).filter(models.User.instagram_profile == user.instagram_profile).first():
        raise HTTPException(status_code=400, detail="This Instagram profile is already linked to an account.")

    # Check TikTok
    if user.tiktok_profile and db.query(models.User).filter(models.User.tiktok_profile == user.tiktok_profile).first():
        raise HTTPException(status_code=400, detail="This TikTok profile is already linked to an account.")

    # Check Upwork
    if user.upwork_profile and db.query(models.User).filter(models.User.upwork_profile == user.upwork_profile).first():
        raise HTTPException(status_code=400, detail="This Upwork profile is already linked to an account.")

    # Check Fiverr
    if user.fiverr_profile and db.query(models.User).filter(models.User.fiverr_profile == user.fiverr_profile).first():
        raise HTTPException(status_code=400, detail="This Fiverr profile is already linked to an account.")

    # --- 2. DATABASE PERSISTENCE ---
    
    db_user = models.User(**user.model_dump())
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        # Final safety net in case of simultaneous requests
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A database integrity error occurred. One of your unique fields might already exist."
        )

# --- REVIEWS ---
@app.get("/reviews/", response_model=List[schemas.ReviewsResponse])
def read_reviews(db: Session = Depends(get_db)):
    return db.query(models.Reviews).order_by(desc(models.Reviews.review_id)).all()

@app.post("/reviews/", response_model=schemas.ReviewsResponse)
def create_review_and_assign_randomly(review: schemas.ReviewsCreate, db: Session = Depends(get_db)):
    # 1. Prepare the Review object (do NOT commit yet)
    db_review = models.Reviews(**review.model_dump())
    db.add(db_review)
    
    # We flush here so PostgreSQL generates the ID, but doesn't "finish" the save yet
    db.flush() 

    # 2. Pick a random user
    random_user = db.query(models.User).order_by(func.random()).first()

    if not random_user:
        db.rollback()
        raise HTTPException(status_code=404, detail="No users found to assign this review to.")

    # 3. Prepare the link
    new_link = models.UserReview(
        user_id=random_user.id, 
        review_id=db_review.review_id
    )
    db.add(new_link)

    # 4. ONE COMMIT for everything
    try:
        db.commit()
        db.refresh(db_review)
        return db_review
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error.")

# --- USER-REVIEWS ---
@app.get("/user-reviews/", response_model=List[schemas.UserReviewResponse])
def get_user_reviews(db: Session = Depends(get_db)):
    return db.query(models.UserReview).all()


# @app.post("/user-reviews/", response_model=schemas.UserReviewResponse)
# def link_review(link: schemas.UserReviewCreate, db: Session = Depends(get_db)):
#     db_link = models.UserReview(**link.model_dump())
#     db.add(db_link)
#     db.commit()
#     db.refresh(db_link)
#     return db_link