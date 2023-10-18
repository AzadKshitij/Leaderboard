from typing import Optional
from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    pass


# Properties to receive on User creation
class UserCreate(UserBase):
    pass


# Properties to receive on User update
class UserUpdate(UserBase):
    pass


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    pass