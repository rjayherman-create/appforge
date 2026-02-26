from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud.item_crud import get_items, create_item, delete_item

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/")
def list_items(db: Session = Depends(get_db)):
    return get_items(db)

@router.post("/")
def add_item(data: dict, db: Session = Depends(get_db)):
    return create_item(db, data)

@router.delete("/{item_id}")
def remove_item(item_id: int, db: Session = Depends(get_db)):
    return delete_item(db, item_id)
