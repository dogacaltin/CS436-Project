import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/thermal-imprint-459211-c7-500ba9fb2a6d.json"

from google.cloud import firestore

db = firestore.Client()

users = db.collection("users")
singers = db.collection("singers")
albums = db.collection("albums")
songs = db.collection("songs")
logs = db.collection("logs")
