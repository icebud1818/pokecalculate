import os
import json
import re

import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    if os.getenv("FIREBASE_SERVICE_ACCOUNT"):
        service_account_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
        cred = credentials.Certificate(service_account_info)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")
        cred = credentials.Certificate(KEY_PATH)

    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to get the last Pack Value by Set Number
def get_last_pack_value(set_number):
    doc_ref = db.collection("sets").document(str(set_number))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("packValue")
    return None  # if document doesn't exist

# Function to get the set name by Set Number
def get_set_name(set_number):
    doc_ref = db.collection("sets").document(str(set_number))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("setName")
    return None  # if document doesn't exist

def clean_card_name(name):
    # Remove everything from the first " - " onward (space-hyphen-space, not bare hyphens)
    name = re.sub(r'\s+-\s+.*$', '', name)
    # Remove card numbers/codes in parentheses (like "(114 Full Art)" or "(H28)")
    name = re.sub(r'\s*\([^)]+\)\s*$', '', name)
    # Remove (Secret) and similar parentheticals at the end
    name = re.sub(r'\s*\(Secret\)\s*$', '', name, flags=re.IGNORECASE)
    # Remove any trailing whitespace
    name = name.strip()
    return name

COLLECTR_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjZlYThjYzhlLTFjYWUtNDIwMS1iOGM1LTI5NWZhNDI2N2UzMiIsImRhdGUiOiIyMDI2LTAzLTMwVDAyOjQ1OjA1LjAzOFoifQ.YfwO3dkfWBb1pZ0jV2_-nA2x3QqHbLyPBS3l_5rAMDY"
COLLECTR_COLLECTION_ID = "6ea8cc8e-1cae-4201-b8c5-295fa4267e32"
COLLECTR_COLLECTION_PARAM = "a6faf9b7-c8a3-442b-985e-41e37fbf6e71"

COLLECTR_HEADERS = {
    "authorization": COLLECTR_TOKEN,
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://app.getcollectr.com",
    "referer": "https://app.getcollectr.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
}