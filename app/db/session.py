from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.core.config import config

engine = create_engine(
   config.get("SQLALCHEMY_DATABASE_URL"), connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)