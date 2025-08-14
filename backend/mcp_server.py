from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from google_photos_core import get_photos

app = FastAPI()

# Tool input schema
class PhotoRequest(BaseModel):
    limit: Optional[int] = 10

# Tool output schema
class PhotoItem(BaseModel):
    filename: str
    baseUrl: str
    creationTime: str

# Tool execution endpoint
@app.post("/tools/get_google_photos", response_model=List[PhotoItem])
def run_get_photos(request: PhotoRequest):
    return get_photos(limit=request.limit)

# Metadata for MCP tool discovery
@app.get("/.well-known/ai-plugin.json")
def plugin_metadata():
    return {
        "schema_version": "v1",
        "name_for_human": "Google Photo Picker",
        "name_for_model": "get_google_photos",
        "description_for_human": "Get recent photos from your Google Photos",
        "description_for_model": "Use this tool to retrieve up to 10 recent personal photos",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "http://localhost:8000/openapi.json"
        }
    }
