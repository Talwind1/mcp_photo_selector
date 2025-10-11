from fastapi import FastAPI, request
from fastapi.responses import RedirectResponse, JSONResponse
import google_photos_core as core

app = FastAPI()

@app.get("/auth/google")
def auth_google():
    url = core.build_auth_url() 
    return RedirectResponse(url)


@app.get("/photos")
def fetch_photos():
    print("fetching photos")
    return get_photos()
