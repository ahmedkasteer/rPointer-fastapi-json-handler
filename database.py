from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

#config for database
SQLALCHEMY_DATABASE_URL = "postgresql://ahmedkasteer@localhost:5432/postgres"

#creating the engine 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#create a session factory
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind = engine)

Base = declarative_base()

#dependency to get a dataabse session in our routes 
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
