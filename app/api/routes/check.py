from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models.event import Event
from app.api import deps

router = APIRouter()

@router.get("/")
def check():
    return {"message": "Check Working"}