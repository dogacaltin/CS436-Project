from google.cloud import firestore

# Firestore istemcisi oluştur
db = firestore.Client()

# Şarkılar ve puanlar için koleksiyon referansları
songs_ref = db.collection("songs")
ratings_ref = db.collection("ratings")