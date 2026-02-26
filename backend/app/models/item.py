from sqlalchemy import Column, String, Float
from app.db import Base
from app.models.base_model import BaseModel

class Item(Base, BaseModel):
    __tablename__ = "items"

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
