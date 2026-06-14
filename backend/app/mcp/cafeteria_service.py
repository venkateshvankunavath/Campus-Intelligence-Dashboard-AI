"""Cafeteria MCP Server — daily menu with today filter and category filter."""
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.database import get_db
from app.models import MenuItem
from app.schemas import MenuItemCreate, MenuItemOut

router = APIRouter(prefix="/cafeteria", tags=["Cafeteria MCP"])


def _get_menu(db: Session, category: str | None = None, on: date | None = None):
    query = db.query(MenuItem)
    if on:
        query = query.filter(MenuItem.served_on == on)
    if category:
        query = query.filter(MenuItem.category == category.lower())
    return query.order_by(MenuItem.category).all()


@router.get("/menu", response_model=list[MenuItemOut])
def get_menu(category: str | None = None, today: bool = True, db: Session = Depends(get_db)):
    return _get_menu(db, category, date.today() if today else None)


@router.post("/menu", response_model=MenuItemOut, dependencies=[Depends(require_admin)])
def add_menu_item(payload: MenuItemCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["served_on"] = data.get("served_on") or date.today()
    item = MenuItem(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def tool_search_menu(db: Session, query: str) -> str:
    """Agent entry point for cafeteria questions — defaults to today's menu."""
    q = query.lower()
    category = next((c for c in ("breakfast", "lunch", "dinner", "snacks") if c in q), None)
    items = _get_menu(db, category, date.today())
    if not items:
        return "No menu items found for today."
    for it in items:
        it.popularity = (it.popularity or 0) + 1
    db.commit()
    by_cat: dict[str, list[str]] = {}
    for it in items:
        veg = "🟢" if it.is_vegetarian else "🔴"
        by_cat.setdefault(it.category.title(), []).append(f"{veg} {it.name} (₹{it.price:.0f})")
    out = [f"Today's menu ({date.today():%d %b}):"]
    for cat, names in by_cat.items():
        out.append(f"{cat}: " + ", ".join(names))
    return "\n".join(out)
