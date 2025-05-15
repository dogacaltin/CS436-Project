import os
from google.cloud import firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/var/secrets/google/key.json"

db = firestore.Client()
songs = db.collection("songs")
albums = db.collection("albums")
singers = db.collection("singers")
users = db.collection("users")
logs = db.collection("logs")
