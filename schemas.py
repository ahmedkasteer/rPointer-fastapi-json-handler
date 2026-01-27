from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
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

    @field_validator('wink_score')
    @classmethod
    def validate_wink_score(cls, v: int):
        if not (50 <= v <= 80):
            raise ValueError("wink score should be between 50 and 80.")
        return v

    # Custom Validator for Avg Rating Message
    @field_validator('avg_rating')
    @classmethod
    def validate_avg_rating(cls, v: float):
        if not (3.0 <= v <= 4.0):
            raise ValueError("average rating should be either 3.00 or 4.00.")
        return v

    # Custom Validator for Credibility Score (Strict 3 or 4)
    @field_validator('avg_credibility_score')
    @classmethod
    def validate_credibility(cls, v: int):
        if v not in [3, 4]:
            raise ValueError("average credibility score can only be 3 or 4.")
        return v

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
    reviewer_rating: int = Field(..., description="Rating must be 4 or 5")
    
    # We still keep the Field constraints for extra security
    reviewer_comment: str = Field(..., max_length=1500)
    response_reviewer_comment: Optional[str] = Field(None)
    summary: Optional[str] = Field(None)
    time_posted: str = Field(..., max_length=50)

    # Custom Message for Reviewer Comment
    # @field_validator('reviewer_comment')
    # @classmethod
    # def validate_reviewer_comment(cls, v: str):
    #     if not (250 <= len(v) <= 1500):
    #         raise ValueError("reviewer comment should be between 250 and 300 characters.")
    #     return v

    # # Custom Message for Response Comment
    # @field_validator('response_reviewer_comment')
    # @classmethod
    # def validate_response_comment(cls, v: Optional[str]):
    #     if v and not (250 <= len(v) <= 1500):
    #         raise ValueError("response reviewer comment should be between 250 and 300 characters.")
    #     return v

    # @field_validator('reviewer_rating')
    # @classmethod
    # def validate_rating(cls, v: int):
    #     if v not in [4, 5]:
    #         raise ValueError("reviewer rating should be either 4 or 5.")
    #     return v

class ReviewsCreate(ReviewsBase):
    pass

class ReviewsResponse(ReviewsBase):
    review_id: int
    class Config:
        from_attributes = True

# --- USER-REVIEW SCHEMAS ---
class UserReviewBase(BaseModel):
    subject_id: int   
    reviewer_id: int  
    review_id: int

class UserReviewCreate(UserReviewBase):
    pass  # Used for POST requests

class UserReviewResponse(UserReviewBase):
    userreview_id: int  # The primary key from your DB model

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models