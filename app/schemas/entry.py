from typing import Optional
from pydantic import BaseModel


# Shared properties
class EntryBase(BaseModel):
    name: str
    time: float
    date_updated: Optional[str] = None
    owner_id: int

# Properties to receive on entry creation
class EntryCreate(EntryBase):
    name: str
    time: float
    owner_id: int


# Properties to receive on entry update
class EntryUpdate(EntryBase):
    time: float


# Properties shared by models stored in DB
class EntryInDBBase(EntryBase):
    id: int
    name: str
    time: float
    owner_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Entry(EntryInDBBase):
    pass


# Properties properties stored in DB
class EntryInDB(EntryInDBBase):
    pass