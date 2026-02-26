from sqlalchemy.orm import Session
from appforge.models.item import Item

def get_items(db: Session):
    return db.query(Item).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, data: dict):
    item = Item(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = get_item(db, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item
