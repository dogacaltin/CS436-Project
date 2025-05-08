# seed_songs.py

from google.cloud import firestore

# Firestore istemcisi
db = firestore.Client()

# Koleksiyon referansı
songs_ref = db.collection("songs")

# Örnek şarkılar
sample_songs = [
    {"song_id": "s1", "name": "Bohemian Rhapsody", "group_name": "Queen"},
    {"song_id": "s2", "name": "Stairway to Heaven", "group_name": "Led Zeppelin"},
    {"song_id": "s3", "name": "Imagine", "group_name": "John Lennon"},
    {"song_id": "s4", "name": "Smells Like Teen Spirit", "group_name": "Nirvana"},
    {"song_id": "s5", "name": "Hey Jude", "group_name": "The Beatles"},
]

# Ekleme işlemi
for song in sample_songs:
    doc_ref = songs_ref.document(song["song_id"])
    doc_ref.set(song)

print("✅ Sample songs added to Firestore.")