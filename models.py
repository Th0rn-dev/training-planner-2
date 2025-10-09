from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    preview_image_url = Column(String(255))
    video_url = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    comment = Column(Text)
    user = relationship("User")
    card = relationship("Card")