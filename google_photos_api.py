from fastapi import FastAPI

app = FastAPI()

from google_photos_core import get_photos

@app.get("/photos")
def fetch_photos():
    return get_photos()
