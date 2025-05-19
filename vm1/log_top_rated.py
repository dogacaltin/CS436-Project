from google.cloud import firestore
import time

db = firestore.Client()

def log_top_songs():
    print("Fetching top-rated songs...")
    songs_ref = db.collection('songs')
    docs = songs_ref.order_by('avgRateSong', direction=firestore.Query.DESCENDING).limit(5).stream()

    print("\n🎵 Top 5 Songs:")
    for doc in docs:
        data = doc.to_dict()
        name = data.get('name', 'Unnamed')
        rating = data.get('avgRateSong', 'N/A')
        print(f"{name} - Avg Rating: {rating}")
    print("-" * 40)

if __name__ == "__main__":
    while True:
        log_top_songs()
        time.sleep(60)
