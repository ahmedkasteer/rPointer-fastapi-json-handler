from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean,Numeric
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    profile_type = Column(String(20))
    sub_profile_type = Column(String(20))
    bio = Column(Text)
    profile_photo = Column(Text)
    instagram_profile = Column(Text)
    gender = Column(String(20))
    fiverr_profile = Column(Text)
    upwork_profile = Column(Text)
    tiktok_profile = Column(Text)
    personal_website = Column(Text)
    verification_status = Column(Boolean)
    wink_score = Column(Integer)
    avg_rating = Column(Numeric(3, 2))
    avg_credibility_score = Column(Integer)
    created_at = Column(DateTime)

class Reviews(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    reviewer_rating = Column(Integer)
    reviewer_comment = Column(Text)
    response_reviewer_comment = Column(Text)
    summary = Column(Text)
    time_posted = Column(String(50))

class UserReview(Base):
    __tablename__ = "userreview"
    userreview_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    review_id = Column(Integer, ForeignKey("reviews.review_id"))

