import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Base

load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
