import firebase_admin
from firebase_admin import credentials
import os

def ensure_firebase_initialized():
    if not firebase_admin._apps:
        cred_path = os.path.join('firebase', 'service-account.json')  # Adjust if needed
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
