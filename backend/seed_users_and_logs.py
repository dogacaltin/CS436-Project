import random
from firestore_config import users, logs, songs, albums, singers
from ratings import submit_rating
from models import RatingRequest

# --- Helper Functions from fetch.py ---
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

# --- Seeder Functions ---
def generate_mock_users(n=10):
    return [{"nick": f"user_{i}", "password": "test123"} for i in range(1, n + 1)]

def seed_users():
    mock_users = generate_mock_users()
    for user in mock_users:
        doc_ref = users.document()  # create new document each time
        user["proID"] = doc_ref.id
        doc_ref.set({
            "nick": user["nick"],
            "password": user["password"]
        })
        print(f"👤 Created user: {user['nick']}")
    return mock_users

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

        # Update album avg
        song_doc = songs.document(song_id).get().to_dict()
        album_id = song_doc.get("albumID")
        if album_id:
            album_avg = calculate_album_avg(album_id)
            if album_avg is not None:
                albums.document(album_id).update({"avgRateAlbum": album_avg})
                print(f"📀 Updated avgRateAlbum for {album_id}: {album_avg:.2f}")

            # Update singer avg
            album_doc = albums.document(album_id).get().to_dict()
            sid = album_doc.get("sid")
            if sid:
                singer_avg = calculate_singer_avg(sid)
                if singer_avg is not None:
                    singers.document(sid).update({"avgRateSinger": singer_avg})
                    print(f"🎤 Updated avgRateSinger for {sid}: {singer_avg:.2f}")

# --- Run It ---
if __name__ == "__main__":
    print("🚀 Seeding users...")
    users_with_ids = seed_users()

    print("🎵 Fetching all songs from Firestore...")
    song_docs = songs.stream()
    song_ids = [doc.id for doc in song_docs]

    if not song_ids:
        print("⚠️ No songs found in Firestore. Please run spotify_importer.py first.")
    else:
        print("📝 Seeding logs + updating averages...")
        seed_logs(users_with_ids, song_ids)

        print("\n✅ Seeding complete.")
