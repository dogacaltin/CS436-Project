from firestore_config import logs, songs
from models import RatingRequest

# Kullanıcının şarkıya puan vermesi
def submit_rating(data: RatingRequest):
    logs.add(data.dict())
    update_song_avg(data.songID)

# Şarkının ortalama puanını güncelle
def update_song_avg(song_id: str):
    rating_docs = logs.where("songID", "==", song_id).stream()
    ratings = [doc.to_dict()["rate"] for doc in rating_docs]
    if ratings:
        avg = sum(ratings) / len(ratings)
        avg = round(avg, 2)  
        songs.document(song_id).update({"avgRateSong": avg})
        return avg
    return None