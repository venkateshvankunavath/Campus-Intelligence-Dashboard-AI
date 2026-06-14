"""Pydantic v2 schemas for request/response validation."""
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Auth ----------
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: StudentOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- Library ----------
class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    total_copies: int = 1
    available_copies: int = 1


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    request_count: int = 0


# ---------- Events ----------
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    starts_at: datetime
    ends_at: Optional[datetime] = None


class EventCreate(EventBase):
    pass


class EventOut(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    attendance_count: int = 0


# ---------- Cafeteria ----------
class MenuItemBase(BaseModel):
    name: str
    category: str = "lunch"
    description: Optional[str] = None
    price: float = 0.0
    is_vegetarian: bool = True
    served_on: Optional[date] = None


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemOut(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    popularity: int = 0


# ---------- Academics ----------
class NoticeBase(BaseModel):
    title: str
    body: Optional[str] = None
    category: str = "general"


class NoticeCreate(NoticeBase):
    pass


class NoticeOut(NoticeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    published_at: datetime


# ---------- Chat / Agent ----------
class ChatRequest(BaseModel):
    message: str
    student_id: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str
    tool_used: Optional[str] = None
    sources: list[str] = []


class ChatHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: str
    content: str
    tool_used: Optional[str] = None
    created_at: datetime
