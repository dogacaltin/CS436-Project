from fastapi import FastAPI
from models import Rating
from database import db, songs_ref, ratings_ref
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # GCP'ye deploy edince domain bazlı daralt
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/songs")
def get_songs():
    songs = [doc.to_dict() for doc in songs_ref.stream()]
    return songs

# Kullanıcıdan rating al
@app.post("/rate")
def rate_song(rating: Rating):
    ratings_ref.add(rating.dict())
    return {"message": "Rating submitted."}

# Belirli şarkının ortalama puanını döndür
@app.get("/average/{song_id}")
def get_average(song_id: str):
    all_ratings = ratings_ref.where("song_id", "==", song_id).stream()
    scores = [r.to_dict()["rating"] for r in all_ratings]
    if scores:
        return {"average": sum(scores) / len(scores)}
    return {"average": None}