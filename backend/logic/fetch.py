from firestore_config import songs, albums, singers

# Tüm şarkıları getir
def fetch_all_songs():
    return [doc.to_dict() | {"id": doc.id} for doc in songs.stream()]

# Şarkıcının ortalama puanını getir (hesapla)
def fetch_singer_avg(sid: str):
    album_ids = [a.id for a in albums.where("sid", "==", sid).stream()]
    singer_songs = [doc.to_dict() for doc in songs.stream() if doc.to_dict().get("albumID") in album_ids]
    ratings = [s.get("avgRateSong", 0) for s in singer_songs if "avgRateSong" in s]
    if not ratings:
        return None
    return sum(ratings) / len(ratings)

# Albümün ortalamasını getir (hesapla)
def fetch_album_avg(album_id: str):
    album_songs = [doc.to_dict() for doc in songs.where("albumID", "==", album_id).stream()]
    ratings = [s.get("avgRateSong", 0) for s in album_songs if "avgRateSong" in s]
    if not ratings:
        return None
    return sum(ratings) / len(ratings)

# Belirli şarkıcının şarkılarını getir
def fetch_singer_songs(sid: str):
    album_ids = [a.id for a in albums.where("sid", "==", sid).stream()]
    return [doc.to_dict() | {"id": doc.id} for doc in songs.stream() if doc.to_dict().get("albumID") in album_ids]