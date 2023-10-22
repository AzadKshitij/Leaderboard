from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# Shared properties
class EntryBase(BaseModel):
    data: str

# Properties to receive on entry creation
class EntryCreate(EntryBase):
    data: str


# Properties to receive on entry update
class EntryUpdate(EntryBase):
    data: str


# Properties shared by models stored in DB
class EntryInDBBase(EntryBase):
    id: int
    data: str
    user_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class EntryOut(EntryInDBBase):
    pass


# Properties properties stored in DB
class EntryInDB(EntryInDBBase):
    pass