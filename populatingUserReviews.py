from sqlalchemy.orm import Session
from database import SessionLocal
import models
import random

def populate_junction_table():
    db = SessionLocal()
    try:
        # 1. Fetch all 100 users and all 100 reviews
        all_users = db.query(models.User).all()
        all_reviews = db.query(models.Reviews).all()

        if len(all_users) < 2:
            print("Need at least 2 users to assign reviewers!")
            return

        print(f"Assigning 5 random user+review combos to each of the {len(all_users)} subjects...")

        for subject in all_users:
            # Pick 5 random Reviewers (excluding the subject themselves so they don't review themselves)
            potential_reviewers = [u for u in all_users if u.id != subject.id]
            random_reviewers = random.sample(potential_reviewers, 5)
            
            # Pick 5 random Review contents
            random_reviews = random.sample(all_reviews, 5)

            for i in range(5):
                new_entry = models.UserReview(
                    subject_id=subject.id,           # The person getting the review
                    reviewer_id=random_reviewers[i].id, # The person giving the review
                    review_id=random_reviews[i].review_id # The actual review data
                )
                db.add(new_entry)

        db.commit()
        print("Successfully populated the three-way junction table!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_junction_table()