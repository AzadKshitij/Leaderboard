from sqlalchemy import JSON, Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Entry(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data = Column(JSON(), index=True)
    date_updated  = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="entry")