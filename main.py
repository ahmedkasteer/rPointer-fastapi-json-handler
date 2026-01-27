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

from sqlalchemy import func # Add this to your imports at the top

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # --- 1. PRE-CHECKS FOR UNIQUENESS (Keep your existing checks here) ---
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    # ... (Keep all your other uniqueness checks for Instagram, TikTok, etc.)

    # --- 2. DATABASE PERSISTENCE ---
    db_user = models.User(**user.model_dump())
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)

        # --- 3. AUTOMATIC REVIEW ASSIGNMENT (NEW LOGIC) ---
        # Get 5 random reviews from the reviews table
        random_reviews = db.query(models.Reviews).order_by(func.random()).limit(5).all()

        # Get 5 random users to act as "Reviewers" (excluding the new user themselves)
        random_reviewers = db.query(models.User).filter(models.User.id != db_user.id).order_by(func.random()).limit(5).all()

        # Check if we have enough data to perform the assignment
        if len(random_reviewers) >= 5 and len(random_reviews) >= 5:
            for i in range(5):
                new_junction_entry = models.UserReview(
                    subject_id=db_user.id,           # The new user (David)
                    reviewer_id=random_reviewers[i].id, # A random "author"
                    review_id=random_reviews[i].review_id # The review content
                )
                db.add(new_junction_entry)
            
            db.commit() # Save the 5 new review links

        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A database integrity error occurred."
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
def get_user_reviews(
    db: Session = Depends(get_db)
):
    reviews = db.query(models.UserReview).all()
    return reviews

# @app.post("/user-reviews/", response_model=schemas.UserReviewResponse)
# def link_review(link: schemas.UserReviewCreate, db: Session = Depends(get_db)):
#     db_link = models.UserReview(**link.model_dump())
#     db.add(db_link)
#     db.commit()
#     db.refresh(db_link)
#     return db_link

#@app.put() for updation 
#@app.delete for deletion 
#remember to use db.commit <------------

#bcrypt for password hashing 
#pip install bcrypt 
#pip install passlib


"""
DOCUMENT!!!! IGNORE this is for DEVELOPER!!!


from passlib import CryptContext 
pwd_cxt = CryptContext(schema = ["bcrypt], deprecated = 'auto')
hashedPassword = pwd_cxt.hash(request.password)
new_user = models.User(name=request.name, email=request.email, password = hashed.password)
class Hash():
    def bcrypt(password: str)
    return pwd.cxt.hash(request.password)
import from Hash ---- 


use routers to manage large files to prevent main from getting messy. 
routers help users to create and manage large files. 
instead of simply using app instance of making the endpoints for get post put delete
we can simply create an instance router = APIRouter()
and then we can use it to manage large files. 
we then replace for e.g @app.get with @router.get 
this will help modify the methods and make them more manageable for you. 


using prefix allows us to not type the specific endpoints again and again
router = APIRouter()
prefix=("/blog",
tags=['Blogs']
)
"""