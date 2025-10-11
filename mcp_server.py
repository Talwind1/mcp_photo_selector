from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from .google_photos_core import get_photos
from .config import config

app = FastAPI()

app.post("/photos")