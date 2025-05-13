from fastapi import FastAPI
from models import RatingRequest
from firestore_config import db, logs, songs, albums, singers

app = FastAPI()


@app.get("/songs")
def get_all_songs():
    return [doc.to_dict() for doc in songs.stream()]


@app.post("/rate")
def rate_song(data: RatingRequest):
    # Rating log kaydı oluştur
    logs.add(data.dict())

    # Şarkı ortalamasını güncelle
    song_logs = logs.where("songID", "==", data.songID).stream()
    ratings = [doc.to_dict()["rate"] for doc in song_logs]
    avg = sum(ratings) / len(ratings)
    songs.document(data.songID).update({"avgRateSong": avg})
    return {"message": "Rating submitted", "new_avg": avg}


@app.get("/singers/{sid}/avg")
def get_singer_avg(sid: str):
    # Albümleri bul
    album_ids = [a.id for a in albums.where("sid", "==", sid).stream()]
    # Albümlere ait şarkıları bul
    singer_songs = [doc.to_dict() for doc in songs.stream() if doc.to_dict()["albumID"] in album_ids]
    ratings = [s.get("avgRateSong", 0) for s in singer_songs if "avgRateSong" in s]
    if not ratings:
        return {"avgRateSinger": None}
    avg = sum(ratings) / len(ratings)
    singers.document(sid).update({"avgRateSinger": avg})
    return {"avgRateSinger": avg}