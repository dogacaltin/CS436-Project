from fastapi import FastAPI
from models import RatingRequest
from firestore_config import db, logs, songs, albums, singers
from fastapi import HTTPException
from models import LoginRequest, SignupRequest
import uuid
from firestore_config import users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # veya ["http://localhost:3000"] gibi daha güvenli bir ayar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/signup")
def signup(data: SignupRequest):
    # Aynı nick varsa reddet
    existing = users.where("nick", "==", data.nick).stream()
    if any(existing):
        raise HTTPException(status_code=400, detail="Nickname already in use")

    pro_id = str(uuid.uuid4())  # benzersiz kullanıcı ID

    users.document(pro_id).set({
        "proID": pro_id,
        "nick": data.nick,
        "password": data.password  # ileride hashle
    })

    return {"message": "User created", "proID": pro_id}


@app.post("/login")
def login(data: LoginRequest):
    print(f"Trying to login: {data.nick} - {data.password}")

    matches = users.where("nick", "==", data.nick).where("password", "==", data.password).stream()
    found = False

    for doc in matches:
        found = True
        print("Login match found:", doc.to_dict())
        return {"message": "Login successful", "proID": doc.to_dict()["proID"]}

    if not found:
        print("Login failed: no match found")
    raise HTTPException(status_code=401, detail="Invalid credentials")