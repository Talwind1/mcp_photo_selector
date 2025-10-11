import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
import requests


SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_credentials():
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI") 
    print(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0, open_browser=False)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_photos(limit=10):
    creds = get_credentials()
    headers = {"Authorization": f"Bearer {creds.token}"}
    response = requests.get(
        f"https://photoslibrary.googleapis.com/v1/mediaItems?pageSize={limit}",
        headers=headers
    )
    response.raise_for_status()
    items = response.json().get("mediaItems", [])
    return [
        {
            "filename": item["filename"],
            "baseUrl": item["baseUrl"],
            "creationTime": item["mediaMetadata"]["creationTime"]
        }
        for item in items
    ]