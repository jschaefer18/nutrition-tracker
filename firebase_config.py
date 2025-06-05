# This file initializes the Firebase Admin SDK with your service account credentials.
# It sets up the Firestore database connection used throughout the app.
# Should only be called once during the app lifecycle to avoid initialization errors.

import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
