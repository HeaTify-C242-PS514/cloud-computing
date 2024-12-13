from google.cloud import firestore
import os

# Set path to the Google Cloud credentials dynamically from an environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./capstone-test-443716-0f00e066d4e2.json")
db = firestore.Client()

def save_to_firestore(collection: str, document_id: str, data: dict):
    try:
        db.collection(collection).document(document_id).set(data)
    except Exception as e:
        raise Exception(f"Failed to save data: {e}")
