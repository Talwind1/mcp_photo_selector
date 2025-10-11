import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


BASE_DIR = os.path.dirname(__file__)
CRED_PATH = os.path.join(BASE_DIR, "config", "desktop_credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]

print("PWD:", os.getcwd())
print("CRED_PATH:", CRED_PATH)
print("TOKEN_PATH:", TOKEN_PATH)

# התחלה נקייה: מחיקת הטוקן הישן (פעם אחת)
try:
    os.remove(TOKEN_PATH)
    print("Deleted old token.json")
except FileNotFoundError:
    pass

flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
creds = flow.run_local_server(
    host="localhost", port=8765,
    prompt="consent", access_type="offline", include_granted_scopes="true"
)

print("SCOPES GRANTED:", sorted(list(creds.scopes or [])))
print("HAS REFRESH:", bool(creds.refresh_token))
print("ACCESS TOKEN (first 12):", (creds.token or "")[:12])
with open(TOKEN_PATH, "w") as f:
    f.write(creds.to_json())


service = build("photoslibrary", "v1", credentials=creds, static_discovery=False)
resp = service.albums().list(pageSize=5).execute()
print("items:", len(resp.get("mediaItems", [])))
