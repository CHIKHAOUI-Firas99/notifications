from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

    
class DeskMaterial(Base):
    __tablename__ = "desk_materials"
    desk_id = Column(Integer, ForeignKey("desks.desk_id"), primary_key=True)
    material_id = Column(Integer, ForeignKey("materials.id"), primary_key=True)