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
from app.models.event import Event
from app.api import deps
from app.schemas.event import EventCreate, EventBase
from app.templates.template import templates

import datetime 

router = APIRouter()

# @router.get("/")
@router.get("/", response_class=HTMLResponse)
async def read_events(request: Request, db: Session = Depends(deps.get_db), ):
    # all events
    # filtered_events =  db.query(Event).all()
    # count according to owner_id
    # filtered_events =  db.query(Event).filter(Event.owner_id == 1).count()
    filtered_events =  db.query(Event).filter(
        Event.eventDate <= datetime.datetime.utcnow()).filter(
        Event.eventDate >= datetime.datetime.utcnow() - datetime.timedelta(days=7)
        ).all()
    logger.warning(jsonable_encoder(filtered_events))
    return templates.TemplateResponse("event.jinja-html",
                                      { "request": request,
                                        "events": jsonable_encoder(filtered_events),
                                        "name": "Event"})
    # return jsonable_encoder(filtered_events)

@router.get("/{owner_id}")
async def read_owner_events(
    owner_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve items.
    """
    # db.query(Event).filter(Event.owner_id == owner_id).all()
    # return db.query(Event).filter(Event.owner_id == owner_id).all()
    return jsonable_encoder(db.query(Event).filter(Event.owner_id == owner_id).all())
    # return False



@router.post("/{owner_id}")
async def create_item(
    owner_id: int,
    obj_in: EventCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new item.
    """
    logger.info("Creating event")
    logger.info(owner_id)
    logger.info(type(obj_in))
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Event(**obj_in_data, owner_id=owner_id)
    logger.info(db_obj)
    try:
        logger.info("Creating event")
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
    db_obj = db.query(Event).filter(Event.owner_id == owner_id).filter(Event.id == id).first()
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
    db_obj = db.query(Event).filter(Event.owner_id == owner_id).filter(Event.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_obj)
    db.commit()
    return db_obj