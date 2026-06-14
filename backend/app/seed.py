"""Seed the database with demo data so the app is useful immediately."""
from datetime import datetime, timedelta, date

from app.auth.security import hash_password
from app.database import Base, SessionLocal, engine
from app.models import (
    AcademicNotice, Book, Event, MenuItem, Student,
)


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Student).count() > 0:
            print("DB already seeded — skipping.")
            return

        # Users
        db.add_all([
            Student(name="Demo Student", email="student@campus.edu",
                    hashed_password=hash_password("student123"), role="student"),
            Student(name="Admin User", email="admin@campus.edu",
                    hashed_password=hash_password("admin123"), role="admin"),
        ])

        # Books
        db.add_all([
            Book(title="Database System Concepts", author="Silberschatz", isbn="9780078022159",
                 category="DBMS", total_copies=4, available_copies=2, request_count=12),
            Book(title="Operating System Concepts", author="Galvin", isbn="9781118063330",
                 category="OS", total_copies=3, available_copies=0, request_count=9),
            Book(title="Introduction to Algorithms", author="Cormen", isbn="9780262033848",
                 category="Algorithms", total_copies=5, available_copies=5, request_count=20),
            Book(title="Computer Networks", author="Tanenbaum", isbn="9780132126953",
                 category="Networks", total_copies=2, available_copies=1, request_count=7),
        ])

        # Events
        now = datetime.utcnow()
        db.add_all([
            Event(title="Campus Hackathon 2026", description="48-hour build sprint.",
                  location="Main Auditorium", category="Tech",
                  starts_at=now + timedelta(days=5), ends_at=now + timedelta(days=7),
                  attendance_count=240),
            Event(title="Cultural Fest — Sangram", description="Inter-college sports & culture fest.",
                  location="Sports Complex", category="Cultural",
                  starts_at=now + timedelta(days=12), attendance_count=560),
            Event(title="Placement Prep Workshop", description="Resume + DSA mock interviews.",
                  location="Seminar Hall B", category="Career",
                  starts_at=now + timedelta(days=2), attendance_count=85),
        ])

        # Menu (today)
        today = date.today()
        db.add_all([
            MenuItem(name="Masala Dosa", category="breakfast", price=40, is_vegetarian=True,
                     served_on=today, popularity=30),
            MenuItem(name="Paneer Butter Masala", category="lunch", price=90, is_vegetarian=True,
                     served_on=today, popularity=55),
            MenuItem(name="Chicken Biryani", category="lunch", price=120, is_vegetarian=False,
                     served_on=today, popularity=72),
            MenuItem(name="Veg Hakka Noodles", category="dinner", price=80, is_vegetarian=True,
                     served_on=today, popularity=41),
            MenuItem(name="Samosa", category="snacks", price=20, is_vegetarian=True,
                     served_on=today, popularity=60),
        ])

        # Notices
        db.add_all([
            AcademicNotice(title="Mid-Sem Exams Begin July 2", category="exam",
                           body="Mid-semester examinations commence on July 2, 2026."),
            AcademicNotice(title="Minimum 75% Attendance Mandatory", category="attendance",
                           body="Students must maintain 75% attendance to sit for end-sem exams."),
            AcademicNotice(title="Project Submission Deadline", category="deadline",
                           body="Final-year project reports due by July 20, 2026."),
        ])

        db.commit()
        print("✅ Database seeded.")
        print("   student@campus.edu / student123")
        print("   admin@campus.edu   / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
