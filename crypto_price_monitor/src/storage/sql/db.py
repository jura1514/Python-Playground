from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.sql.alert_db import Base
import os

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)

def db_setup():
    Base.metadata.create_all(engine)
