from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Entry(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time = Column(Float(2), index=True)
    date_updated  = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user_name = Column(String, ForeignKey('user.name'))
    user = relationship("User", back_populates="entry")