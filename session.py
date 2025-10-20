import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Base

engine = create_engine(
    f"postgresql://{os.environ.get('db_user')}:{os.environ.get('db_password')}@{os.environ.get('db_host')}/{os.environ.get('db_name')}")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
