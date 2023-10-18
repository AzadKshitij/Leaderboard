import json
from pickle import NONE
from tkinter import E
from typing import Any, List
from venv import logger
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.entry import Entry
from app.api import deps
from app.schemas.entry import EntryCreate, EntryBase
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

@router.get("/{owner_id}")
async def read_owner_Entrys(
    owner_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve items.
    """
    # db.query(Entry).filter(Entry.owner_id == owner_id).all()
    # return db.query(Entry).filter(Entry.owner_id == owner_id).all()
    return jsonable_encoder(db.query(Entry).filter(Entry.owner_id == owner_id).all())
    # return False



@router.post("/{owner_id}")
async def create_item(
    owner_id: int,
    obj_in: EntryCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new item.
    """
    logger.info("Creating Entry")
    logger.info(owner_id)
    logger.info(type(obj_in))
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Entry(**obj_in_data, owner_id=owner_id)
    logger.info(db_obj)
    try:
        logger.info("Try Creating Entry")
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logger.error(e)
        raise e
    return jsonable_encoder(db_obj)



@router.put("/{id}")
async def update_item(
    owner_id: int,
    id: int,
    obj_in,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update an item.
    """
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = db.query(Entry).filter(Entry.owner_id == owner_id).filter(Entry.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = obj_in_data
    for field in db_obj:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.delete("/{id}")
async def delete_item(
    owner_id: int,
    id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete an item.
    """
    db_obj = db.query(Entry).filter(Entry.owner_id == owner_id).filter(Entry.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_obj)
    db.commit()
    return db_obj