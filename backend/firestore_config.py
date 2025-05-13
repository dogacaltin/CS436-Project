from google.cloud import firestore

db = firestore.Client()

# Kolay erişim için referanslar
users = db.collection("users")
singers = db.collection("singers")
albums = db.collection("albums")
songs = db.collection("songs")
logs = db.collection("logs")