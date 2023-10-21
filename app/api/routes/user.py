import json
from typing import Any, List
from venv import logger
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.entry import Entry
from app.models.user import User
from app.api import deps
from app.schemas.user import UserCreate, UserBase

import datetime 

router = APIRouter()



@router.get("/get/{user_id}")
def read_item(
    user_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve items.
    """
    try:
        user_info = db.query(User).filter(
            User.id == user_id).all()
    except Exception as e:
        logger.error(msg= "User not found " + str(e))
        raise HTTPException(status_code=404, detail="User not found")

    return jsonable_encoder(user_info)

# @router.post("/", response_model=user.User)
@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(deps.get_db), ):
        logger.info("Creating user")
        obj_in = jsonable_encoder(user)
        db_obj = User(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj