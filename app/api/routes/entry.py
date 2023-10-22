import json
from pickle import NONE
from tkinter import E
from typing import Any, List
from venv import logger
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.api import deps
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from app.models.entry import Entry
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryBase, EntryOut
# from app.templates.template import templates

import datetime 

router = APIRouter()

# @router.get("/")
# @router.get("/", response_class=HTMLResponse)
# async def read_Entrys(request: Request, db: Session = Depends(deps.get_db), ):
#     # all Entrys
#     # filtered_Entrys =  db.query(Entry).all()
#     # count according to owner_id
#     # filtered_Entrys =  db.query(Entry).filter(Entry.owner_id == 1).count()
#     filtered_Entrys =  db.query(Entry).filter(
#         Entry.EntryDate <= datetime.datetime.utcnow()).filter(
#         Entry.EntryDate >= datetime.datetime.utcnow() - datetime.timedelta(days=7)
#         ).all()
#     logger.warning(jsonable_encoder(filtered_Entrys))
#     return templates.TemplateResponse("Entry.jinja-html",
#                                       { "request": request,
#                                         "Entrys": jsonable_encoder(filtered_Entrys),
#                                         "name": "Entry"})
    # return jsonable_encoder(filtered_Entrys)

@router.get("/get-by-user/{user_id}")
async def read_owner_Entries(
    user_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve entries by user.
    """
    try:
        return jsonable_encoder(db.query(User).filter(User.id == user_id).options(joinedload(User.entry)).first())
    except Exception as e:
        logger.error(msg= "User not found " + str(e))
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/get-by-id/{entry_id}")
async def read_by_id(
    entry_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve entry by id.
    """
    try:
        entry = jsonable_encoder(db.query(Entry).filter(Entry.id == entry_id).first())
        data = json.loads(entry['data'])
        logger.info(f"entry {entry}")
        date = entry['date_updated']
        return {
            "data": data,
            "date": date
        }
    except Exception as e:
        logger.error(msg= "Entry not found " + str(e))
        raise HTTPException(status_code=404, detail="Entry not found")



@router.post("/create/{user_id}")
async def create_item(
    user_id: int,
    obj_in,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new item.
    """
    logger.info(f"'obj_in '{obj_in}")
    user = db.query(User).filter(User.id == user_id).first()
    data = json.dumps(obj_in)
    try:
        db_obj = Entry(data = data, user = user)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info("Entry created")
    except Exception as e:
        logger.error(e)
        raise e
    return jsonable_encoder(db_obj)
    # return obj_in



@router.put("/update/{id}")
async def update_item(
    user_id: int,
    id: int,
    obj_in,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update an item.
    """
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = db.query(Entry).filter(Entry.user_id == user_id).filter(Entry.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = obj_in_data
    for field in jsonable_encoder(db_obj):
        logger.info(f"db_obj {field}")
        if field in update_data:
            logger.info("update_data[field]", update_data[field])
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.delete("/{id}")
async def delete_item(
    user_id: int,
    id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete an item.
    """
    db_obj = db.query(Entry).filter(Entry.user_id == user_id).filter(Entry.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_obj)
    db.commit()
    return db_obj