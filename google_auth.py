import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "config", "desktop_credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]


def load_token():
    """Load token from file if exists, else return None."""
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        return Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    except:
        return None


def save_token(creds):
    """Save credentials to file."""
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())


def do_oauth():
    """Perform OAuth flow (opens browser)."""
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    return flow.run_local_server(
        host="localhost",
        port=8765,
        prompt="consent",
        access_type="offline",
        include_granted_scopes="true"
    )

def get_credentials():
    
    creds = load_token()
    
    if creds and creds.valid:
        print("Using existing token")
        return creds
    
    if creds and creds.expired and creds.refresh_token:
        try:
            print("Refreshing token...")
            creds.refresh(Request())
            save_token(creds)
            print("Token refreshed.")
            return creds
        except:
            pass  

    creds = do_oauth()
    save_token(creds)
    
    return creds


# ============================================================================
# Test
# ============================================================================

def main():
    """Test authentication."""
    creds = get_credentials()

    service = build("photoslibrary", "v1", credentials=creds, static_discovery=False)
    resp = service.albums().list(pageSize=5).execute()
    albums = resp.get("albums", [])
    
    print(f"Found {len(albums)} albums")


if __name__ == "__main__":
    main()