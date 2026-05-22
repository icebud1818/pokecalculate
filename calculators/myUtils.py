import os
import json
import re

import requests
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

COLLECTR_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjZlYThjYzhlLTFjYWUtNDIwMS1iOGM1LTI5NWZhNDI2N2UzMiIsImRhdGUiOiIyMDI2LTA0LTAzVDEzOjI4OjI3LjIxMVoifQ.exWkc5_P4KFguvdRQwJdHQFdaJex1ktjk86EstFrdqg"
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


# Function to get the last Box Value by Set Number
def get_last_box_value(set_number):
    doc_ref = db.collection("boosterBoxes").document(str(set_number))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("boxPrice")
    return None


# ---------------------------------------------------------------------------
# Price-source tracking
#
# Every price-fetching helper below records where the final price came from:
#   "collectr"  — Collectr API returned a price
#   "tcgplayer" — TCGPlayer marketPrice / medianPrice / lowestPrice
#   "previous"  — Falling back to the last value already in Firestore
#   "none"      — All sources failed; no price available
#
# Call print_price_source_summary() at the end of a workflow to render the
# breakdown to stdout and (when running in GitHub Actions) to the step
# summary so it shows up in the run's UI.
# ---------------------------------------------------------------------------

PRICE_SOURCE_LOG = []


def record_price_source(category, name, source, price):
    """Append a price-source entry. `category` is e.g. "pack", "box", "sealed"."""
    PRICE_SOURCE_LOG.append({
        "category": category,
        "name": name,
        "source": source,
        "price": price,
    })


def _try_collectr(product_id):
    try:
        r = requests.get(
            f"https://api-v2.getcollectr.com/collections/{COLLECTR_COLLECTION_ID}/products/{product_id}",
            headers=COLLECTR_HEADERS,
            params={"collectionId": COLLECTR_COLLECTION_PARAM, "currency": "USD", "details": "false"},
            timeout=20,
        )
        if r.status_code == 200:
            price = float(r.json()["data"]["market_price"])
            if price > 0:
                return price
    except Exception:
        pass
    return None


def _try_tcgplayer(product_id):
    try:
        r = requests.get(
            f"https://mp-search-api.tcgplayer.com/v2/product/{product_id}/details?mpfev=3442",
            timeout=20,
        )
        data = r.json()
        return data.get("marketPrice") or data.get("medianPrice") or data.get("lowestPrice")
    except Exception:
        return None


def get_pack_price(product_id, set_number, set_name, sources=("collectr", "tcgplayer")):
    """Try Collectr → TCGPlayer → previous Firestore value (in that order, or as overridden).
    Records the chosen source in PRICE_SOURCE_LOG. Returns price (float) or None."""
    for source in sources:
        price = _try_collectr(product_id) if source == "collectr" else _try_tcgplayer(product_id)
        if price:
            record_price_source("pack", set_name, source, price)
            return price

    prev = get_last_pack_value(set_number)
    if prev is not None:
        record_price_source("pack", set_name, "previous", prev)
        return prev

    record_price_source("pack", set_name, "none", None)
    return None


def get_box_price(product_id, set_number, set_name):
    """TCGPlayer → previous Firestore value. Records source. Returns price or None."""
    price = _try_tcgplayer(product_id)
    if price:
        record_price_source("box", set_name, "tcgplayer", price)
        return price

    prev = get_last_box_value(set_number)
    if prev is not None:
        record_price_source("box", set_name, "previous", prev)
        return prev

    record_price_source("box", set_name, "none", None)
    return None


def print_price_source_summary(category=None, title=None):
    """Print a per-source breakdown of PRICE_SOURCE_LOG to stdout and to the
    GitHub Actions step summary when running in CI."""
    relevant = [e for e in PRICE_SOURCE_LOG if category is None or e["category"] == category]
    if not relevant:
        return

    by_source = {}
    for e in relevant:
        by_source.setdefault(e["source"], []).append(e["name"])

    header = title or (f"Price Source Summary ({category})" if category else "Price Source Summary")
    source_order = ("collectr", "tcgplayer", "previous", "none")

    print(f"\n=== {header} ===")
    print(f"Total items: {len(relevant)}")
    for source in source_order:
        names = by_source.get(source, [])
        if not names:
            continue
        print(f"  {source}: {len(names)}")
        if source != "collectr":
            for n in names:
                print(f"    - {n}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        try:
            with open(summary_path, "a") as f:
                f.write(f"\n## {header}\n\n")
                f.write(f"**Total items:** {len(relevant)}\n\n")
                f.write("| Source | Count | Items |\n")
                f.write("|--------|------:|-------|\n")
                for source in source_order:
                    names = by_source.get(source, [])
                    if not names:
                        continue
                    items_str = "_(all defaults)_" if source == "collectr" else ", ".join(names)
                    f.write(f"| **{source}** | {len(names)} | {items_str} |\n")
        except Exception as e:
            print(f"Warning: could not write to GITHUB_STEP_SUMMARY: {e}")
