from sqlalchemy import Column, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True , index = True)
    email = Column(String(255), unique=True)
    name =Column(String(255))
    demandes = relationship("Demand", uselist=False, back_populates="user", cascade="all, delete-orphan")
    desks = relationship("Reservation", back_populates="user")
