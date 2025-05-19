from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
import random
import requests

from models import RatingRequest, LoginRequest, SignupRequest
from firestore_config import db, logs, songs, albums, singers, users

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/songs")
def get_songs():
    songs_list = []
    for doc in songs.stream():
        song = doc.to_dict()
        song["songID"] = doc.id  
        songs_list.append(song)
    return songs_list

@app.post("/rate")
def rate_song(data: RatingRequest):
    try:
        print("📩 Incoming rating:", data.dict())
        logs.add(data.dict())

        rating_docs = logs.where("songID", "==", data.songID).stream()
        ratings = [doc.to_dict()["rate"] for doc in rating_docs]
        if ratings:
            avg = sum(ratings) / len(ratings)
            songs.document(data.songID).update({"avgRateSong": avg})
            trigger_log_function(data.proID, data.songID, data.rate)

            song_doc = songs.document(data.songID).get()
            if song_doc.exists:
                album_id = song_doc.to_dict().get("albumID")
                if album_id:
                    album_docs = songs.where("albumID", "==", album_id).stream()
                    album_ratings = [d.to_dict().get("avgRateSong", 0) for d in album_docs]
                    if album_ratings:
                        album_avg = sum(album_ratings) / len(album_ratings)
                        albums.document(album_id).update({"avgRateAlbum": album_avg})

                    album_doc = albums.document(album_id).get()
                    if album_doc.exists:
                        sid = album_doc.to_dict().get("sid")
                        if sid:
                            album_ids = [a.id for a in albums.where("sid", "==", sid).stream()]
                            singer_songs = [doc.to_dict() for doc in songs.stream() if doc.to_dict().get("albumID") in album_ids]
                            singer_ratings = [s.get("avgRateSong", 0) for s in singer_songs if "avgRateSong" in s]
                            if singer_ratings:
                                singer_avg = sum(singer_ratings) / len(singer_ratings)
                                singers.document(sid).update({"avgRateSinger": singer_avg})

            return {"message": "Rating submitted", "new_avg": avg}
        else:
            return {"message": "Rating failed"}

    except Exception as e:
        print("🔥 Error in /rate:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/signup")
def signup(data: SignupRequest):
    existing = users.where("nick", "==", data.nick).stream()
    if any(existing):
        raise HTTPException(status_code=400, detail="Nickname already in use")

    pro_id = str(uuid.uuid4())
    users.document(pro_id).set({
        "proID": pro_id,
        "nick": data.nick,
        "password": data.password
    })

    return {"message": "User created", "proID": pro_id}

@app.post("/login")
def login(data: LoginRequest):
    matches = users.where("nick", "==", data.nick).where("password", "==", data.password).stream()
    for doc in matches:
        return {"message": "Login successful", "proID": doc.to_dict()["proID"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/logs/random")
def get_random_logs():
    all_logs = [log.to_dict() for log in logs.stream()]
    if not all_logs:
        return []

    sample_logs = random.sample(all_logs, min(5, len(all_logs)))
    result = []
    for log in sample_logs:
        song_id = log.get("songID")
        rate = log.get("rate")
        song_doc = songs.document(song_id).get()
        song_name = song_doc.to_dict().get("name") if song_doc.exists else "Unknown Song"
        result.append({
            "songName": song_name,
            "rate": rate,
            "songID": song_id
        })
    return result

@app.get("/singers/{sid}/avg")
def get_singer_avg(sid: str):
    album_ids = [a.id for a in albums.where("sid", "==", sid).stream()]
    singer_songs = [doc.to_dict() for doc in songs.stream() if doc.to_dict()["albumID"] in album_ids]
    ratings = [s.get("avgRateSong", 0) for s in singer_songs if "avgRateSong" in s]
    if not ratings:
        return {"avgRateSinger": None}
    avg = sum(ratings) / len(ratings)
    singers.document(sid).update({"avgRateSinger": avg})
    return {"avgRateSinger": avg}

@app.get("/search")
def search_items(query: str = Query(...), type: str = Query(...)):
    results = []

    if type == "song":
        for doc in songs.stream():
            song = doc.to_dict()
            song["songID"] = doc.id  
            if query.lower() in song["name"].lower():
                results.append(song)

    elif type == "artist":
        for doc in singers.stream():
            artist = doc.to_dict()
            artist["sid"] = doc.id
            if query.lower() in artist["name"].lower():
                results.append(artist)

    elif type == "album":
        for doc in albums.stream():
            album = doc.to_dict()
            album["albumID"] = doc.id  
            if query.lower() in album["name"].lower():
                results.append(album)

    return results

@app.get("/albums")
def get_all_albums():
    return [doc.to_dict() | {"albumID": doc.id} for doc in albums.stream()]

@app.get("/albums/{album_id}")
def get_album(album_id: str):
    doc = albums.document(album_id).get()
    if doc.exists:
        data = doc.to_dict()
        data["albumID"] = doc.id
        return data
    raise HTTPException(status_code=404, detail="Album not found")

@app.get("/singers/{sid}")
def get_singer(sid: str):
    doc = singers.document(sid).get()
    if doc.exists:
        return doc.to_dict()
    raise HTTPException(status_code=404, detail="Singer not found")

def trigger_log_function(proID, songID, rate):
    url = "https://us-central1-thermal-imprint-459211-c7.cloudfunctions.net/log_review"
    payload = {
        "proID": proID,
        "songID": songID,
        "rate": rate
    }

    try:
        response = requests.post(url, json=payload)
        print("Log Function Response:", response.text)
    except Exception as e:
        print("Error calling log function:", e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
