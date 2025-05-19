import random
import uuid
from google.cloud import firestore
from dataclasses import dataclass

db = firestore.Client()
users = db.collection("users")
logs = db.collection("logs")
songs = db.collection("songs")
albums = db.collection("albums")
singers = db.collection("singers")

@dataclass
class RatingRequest:
    songID: str
    rate: int
    proID: str

def submit_rating(data: RatingRequest):
    logs.add({
        "songID": data.songID,
        "rate": data.rate,
        "proID": data.proID
    })

def update_avg_rate_for_song(song_id: str):
    song_logs = [doc.to_dict() for doc in logs.where("songID", "==", song_id).stream()]
    ratings = [r["rate"] for r in song_logs if "rate" in r]
    if ratings:
        avg = sum(ratings) / len(ratings)
        songs.document(song_id).update({"avgRateSong": avg})
        return avg
    return None

def calculate_album_avg(album_id: str):
    album_songs = [doc.to_dict() for doc in songs.where("albumID", "==", album_id).stream()]
    ratings = [s.get("avgRateSong", 0) for s in album_songs if "avgRateSong" in s]
    if not ratings:
        return None
    return sum(ratings) / len(ratings)

def calculate_singer_avg(sid: str):
    album_ids = [a.id for a in albums.where("sid", "==", sid).stream()]
    singer_songs = [doc.to_dict() for doc in songs.stream() if doc.to_dict().get("albumID") in album_ids]
    ratings = [s.get("avgRateSong", 0) for s in singer_songs if "avgRateSong" in s]
    if not ratings:
        return None
    return sum(ratings) / len(ratings)

def generate_mock_users(n=10):
    return [{"nick": f"user_{i}_{uuid.uuid4().hex[:5]}", "password": "test123"} for i in range(1, n + 1)]

def seed_users():
    mock_users = generate_mock_users()
    seeded_users = []

    for user in mock_users:
        existing = users.where("nick", "==", user["nick"]).limit(1).stream()
        if any(existing):
            print(f"⚠️ Skipping existing user: {user['nick']}")
            continue

        doc_ref = users.document()
        user["proID"] = doc_ref.id
        doc_ref.set({
            "nick": user["nick"],
            "password": user["password"]
        })
        print(f"👤 Created user: {user['nick']}")
        seeded_users.append(user)

    return seeded_users

def seed_logs(users, song_ids, num_ratings=30):
    for _ in range(num_ratings):
        user = random.choice(users)
        song_id = random.choice(song_ids)
        rating = random.randint(1, 5)

        rating_data = RatingRequest(
            songID=song_id,
            rate=rating,
            proID=user["proID"]
        )
        submit_rating(rating_data)
        print(f"⭐ {user['nick']} rated song {song_id} → {rating}/5")

        avg_song = update_avg_rate_for_song(song_id)
        if avg_song is not None:
            print(f"🎼 Updated avgRateSong for {song_id}: {avg_song:.2f}")

        song_doc = songs.document(song_id).get().to_dict()
        album_id = song_doc.get("albumID")
        if album_id:
            album_avg = calculate_album_avg(album_id)
            if album_avg is not None:
                albums.document(album_id).update({"avgRateAlbum": album_avg})
                print(f"📀 Updated avgRateAlbum for {album_id}: {album_avg:.2f}")

            album_doc = albums.document(album_id).get().to_dict()
            sid = album_doc.get("sid")
            if sid:
                singer_avg = calculate_singer_avg(sid)
                if singer_avg is not None:
                    singers.document(sid).update({"avgRateSinger": singer_avg})
                    print(f"🎤 Updated avgRateSinger for {sid}: {singer_avg:.2f}")

if __name__ == "__main__":
    print("🚀 Seeding users...")
    users_with_ids = seed_users()

    if not users_with_ids:
        print("⚠️ No new users were seeded. Exiting.")
        exit()

    print("🎵 Fetching all songs from Firestore...")
    song_docs = songs.stream()
    song_ids = [doc.id for doc in song_docs]

    if not song_ids:
        print("⚠️ No songs found in Firestore. Please run spotify_importer.py first.")
    else:
        print("📝 Seeding logs + updating averages...")
        seed_logs(users_with_ids, song_ids)

        print("\n✅ Seeding complete.")

