import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Step 1: Set the scope (read-only access to Google Photos)
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_credentials():
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

def list_photos():
    creds = get_credentials()
    service = build('photoslibrary', 'v1', credentials=creds)
    results = service.mediaItems().list(pageSize=10).execute()
    items = results.get('mediaItems', [])
    for item in items:
        print(item['filename'], item['baseUrl'])

if __name__ == '__main__':
    list_photos()
