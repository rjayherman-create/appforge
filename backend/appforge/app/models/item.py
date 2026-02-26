from sqlalchemy import Column, String, Float
from appforge.db import Base
from appforge.models.base_model import BaseModel

class Item(Base, BaseModel):
    __tablename__ = "items"

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
