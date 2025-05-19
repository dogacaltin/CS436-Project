import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.cloud import firestore

# === SPOTIFY API SETUP ===
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# === FIRESTORE SETUP ===
# Make sure to export GOOGLE_APPLICATION_CREDENTIALS before running
db = firestore.Client()
singers_ref = db.collection("singers")
albums_ref = db.collection("albums")
songs_ref = db.collection("songs")

# === FETCH ARTIST ===
artist_name = input("🎤 Enter artist name: ")
results = sp.search(q=artist_name, type="artist", limit=1)

if not results["artists"]["items"]:
    print("❌ Artist not found.")
    exit()

artist = results["artists"]["items"][0]
sid = artist["id"]
genres = artist.get("genres", [])
singer_doc = {
    "name": artist["name"],
    "avgRateSinger": 0,
    "genres": genres
}

singers_ref.document(sid).set(singer_doc)
print(f"✅ Added singer: {artist['name']}")

# === FETCH TOP TRACKS ===
top_tracks = sp.artist_top_tracks(sid)["tracks"]

for track in top_tracks:
    track_id = track["id"]
    track_name = track["name"]
    album = track["album"]
    album_id = album["id"]
    album_name = album["name"]
    release_year = album["release_date"][:4]

    # Save album
    albums_ref.document(album_id).set({
        "sid": sid,
        "name": album_name,
        "year": release_year,
        "genre": genres[0] if genres else "unknown",
        "avgRateAlbum": 0
    })

    # Save song
    songs_ref.document(track_id).set({
        "albumID": album_id,
        "name": track_name,
        "avgRateSong": 0
    })

    print(f"🎵 Added track: {track_name} from album: {album_name}")

print(f"\n✅ Finished importing top tracks for {artist['name']}.")
