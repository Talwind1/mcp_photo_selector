import requests
from dotenv import load_dotenv
import os

ACCESS_TOKEN = "..."  # Token תקף
url = "https://photoslibrary.googleapis.com/v1/albums"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

load_dotenv()
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
print('HHHHI', client_id, client_secret)
res = requests.get(url, headers=headers)
print(res.json())