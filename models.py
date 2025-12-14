import uuid

from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<Role(id={self.id}, name={self.name})>'

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

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

class Card(Base):
    __tablename__ = 'cards'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    preview_image_url = Column(String(255))
    video_url = Column(String(255))
    category_id = Column(PG_UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship("Category")

    def __repr__(self):
        return (f"<Card(id={self.id}, title={self.title}, preview_image_url={self.preview_image_url}, "
                f"video_url={self.video_url}, category_id={self.category_id})>")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('users.id'))
    card_id = Column(PG_UUID(as_uuid=True), ForeignKey('cards.id'))
    comment = Column(Text)
    user = relationship("User")
    card = relationship("Card")