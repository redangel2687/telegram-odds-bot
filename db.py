from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Alert(Base):
__tablename__ = "alerts"
id = Column(Integer, primary_key=True)
user_id = Column(Integer)
match = Column(String)


Base.metadata.create_all(engine)
