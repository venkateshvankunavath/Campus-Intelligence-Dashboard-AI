"""SQLAlchemy ORM models for all campus domains."""
from datetime import datetime, date

from sqlalchemy import (
    Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student", nullable=False)  # student | admin
    created_at = Column(DateTime, default=datetime.utcnow)

    chats = relationship("ChatHistory", back_populates="student", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    author = Column(String(160), index=True)
    isbn = Column(String(20), index=True)
    category = Column(String(80), index=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    request_count = Column(Integer, default=0)  # for "most requested" analytics
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def available(self) -> bool:
        return self.available_copies > 0


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text)
    location = Column(String(160))
    category = Column(String(80), index=True)
    starts_at = Column(DateTime, index=True, nullable=False)
    ends_at = Column(DateTime)
    attendance_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), index=True, nullable=False)
    category = Column(String(40), index=True)  # breakfast | lunch | dinner | snacks
    description = Column(Text)
    price = Column(Float, default=0.0)
    is_vegetarian = Column(Boolean, default=True)
    served_on = Column(Date, index=True, default=date.today)
    popularity = Column(Integer, default=0)  # for menu popularity analytics


class AcademicNotice(Base):
    __tablename__ = "academic_notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    body = Column(Text)
    category = Column(String(80), index=True)  # exam | attendance | general | deadline
    published_at = Column(DateTime, default=datetime.utcnow, index=True)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    role = Column(String(20))  # user | assistant
    content = Column(Text)
    tool_used = Column(String(60), nullable=True)  # which MCP tool the agent picked
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="chats")
