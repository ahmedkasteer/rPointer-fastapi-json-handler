from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, Literal
from datetime import datetime

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    profile_type: Literal["freelancer", "influencer", "client"]
    sub_profile_type: Literal["personal", "company"]
    bio: Optional[str] = None
    profile_photo: Optional[str] = None
    gender: Optional[str] = Field(None, max_length=20)
    fiverr_profile: Optional[str] = None
    upwork_profile: Optional[str] = None
    instagram_profile: Optional[str] = None
    tiktok_profile: Optional[str] = None
    personal_website: Optional[str] = None
    verification_status: bool = False
    wink_score: int = Field(..., ge=50, le=80)
    avg_rating: float # Numeric(3,2) needs float
    avg_credibility_score: int

    @model_validator(mode="after")
    def validate_user_rules(self):
        if self.profile_type == "freelancer" and (self.instagram_profile or self.tiktok_profile):
            raise ValueError("Freelancers cannot have Social Media profiles")
        elif self.profile_type == "influencer" and (self.fiverr_profile or self.upwork_profile):
            raise ValueError("Influencers cannot have Freelance profiles")
        elif self.profile_type == "client" and any([self.fiverr_profile, self.upwork_profile, self.instagram_profile, self.tiktok_profile]):
            raise ValueError("Clients can only have a personal website")
        return self

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None # Fixed: Matches DB column name

    class Config:
        from_attributes = True

# --- REVIEWS SCHEMAS ---
class ReviewsBase(BaseModel):
    reviewer_rating: int = Field(..., ge=4, le=5)
    reviewer_comment: str
    response_reviewer_comment: Optional[str] = None
    summary: Optional[str] = None
    time_posted: str = Field(..., max_length=50)

class ReviewsCreate(ReviewsBase):
    pass

class ReviewsResponse(ReviewsBase):
    review_id: int
    class Config:
        from_attributes = True

# --- USER-REVIEW SCHEMAS ---
class UserReviewCreate(BaseModel):
    user_id: int
    review_id: int

class UserReviewResponse(UserReviewCreate):
    userreview_id: int
    class Config:
        from_attributes = True