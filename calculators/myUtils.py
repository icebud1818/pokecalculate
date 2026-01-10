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

def clean_card_name(name):
    # Remove everything from the first " - " onward (like " - #H28/H32 - $615.95")
    name = re.sub(r'\s*-.*$', '', name)
    # Remove card numbers/codes in parentheses (like "(114 Full Art)" or "(H28)")
    name = re.sub(r'\s*\([^)]+\)\s*$', '', name)
    # Remove (Secret) and similar parentheticals at the end
    name = re.sub(r'\s*\(Secret\)\s*$', '', name, flags=re.IGNORECASE)
    # Remove any trailing whitespace
    name = name.strip()
    return name