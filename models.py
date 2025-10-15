import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role_id = Column(PG_UUID(as_uuid=True), ForeignKey('roles.id'))
    role = relationship("Role")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)

class Card(Base):
    __tablename__ = 'cards'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    preview_image_url = Column(String(255))
    video_url = Column(String(255))
    category_id = Column(PG_UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship("Category")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('users.id'))
    card_id = Column(PG_UUID(as_uuid=True), ForeignKey('cards.id'))
    comment = Column(Text)
    user = relationship("User")
    card = relationship("Card")