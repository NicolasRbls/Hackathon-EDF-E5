import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Default to Docker config, but allow env override
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://edf_user:edf_password@localhost:5432/edf_track"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
