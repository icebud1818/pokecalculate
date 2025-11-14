import firebase_admin
from firebase_admin import credentials, firestore

# ---- INIT FIREBASE ----
# Replace with the correct path to your JSON key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# ---- WRITE EXAMPLE ----
def write_example():
    doc_ref = db.collection("testCollection").document("exampleDoc")
    doc_ref.set({
        "message": "Hello from Python!",
        "number": 42
    })
    print("✅ Data written")


# ---- READ EXAMPLE ----
def read_example():
    doc = db.collection("testCollection").document("exampleDoc").get()
    if doc.exists:
        print("✅ Document data:", doc.to_dict())
    else:
        print("❌ Document not found")


if __name__ == "__main__":
    write_example()
    read_example()
