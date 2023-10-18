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

import datetime 

router = APIRouter()