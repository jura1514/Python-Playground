from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from storage.sql.alert_db import Base

db_url = Config.DATABASE_URL
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)

def db_setup():
    Base.metadata.create_all(engine)
