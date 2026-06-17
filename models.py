import uuid

from sqlalchemy import String, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("roles.id"))
    role = relationship("Role")


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    parent = relationship('Category', remote_side=[id], backref='children')

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, parent_id={self.parent_id})>"


class Card(Base):
    __tablename__ = "cards"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    preview_image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    video_url: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("categories.id"))
    invisible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    category = relationship("Category", backref="cards")

    def __repr__(self):
        return (f"<Card(id={self.id}, title={self.title}, preview_image_url={self.preview_image_url}, "
                f"video_url={self.video_url}, category_id={self.category_id})>")


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    card_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("cards.id"))
    comment: Mapped[str] = mapped_column(Text)
    user = relationship("User")
    card = relationship("Card")


class TrainingSession(Base):
    __tablename__ = 'training_session'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[Date] = mapped_column(Date, nullable=False)
    training_date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    def __repr__(self) -> str:
        return (f"<TrainingSession(id={self.id}, created_at={self.created_at}, training_date={self.training_date}, "
                f"description={self.description})>")


class TrainingAction(Base):
    __tablename__ = 'training_action'

    id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('cards.id'), nullable=True)
    duration: Mapped[int] = mapped_column(nullable=False)
    training_session_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('training_session.id'),
                                                           nullable=False)
    training_session = relationship("TrainingSession")
    card = relationship("Card")

    def __repr__(self) -> str:
        return (f"<TrainingAction(id={self.id}, card_id={self.card_id}, duration={self.duration}, "
                f"training_session_id={self.training_session_id})>")