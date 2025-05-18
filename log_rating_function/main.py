from google.cloud import firestore
from flask import request
from datetime import datetime, timezone

def log_review(request):
    db = firestore.Client()
    req = request.get_json(silent=True)

    try:
        pro_id = req.get("proID")
        song_id = req.get("songID")
        rate = req.get("rate")

        if not all([pro_id, song_id, rate]):
            return "❌ Missing required fields", 400

        # --- Fetch user ---
        user_doc = db.collection("users").document(pro_id).get()
        print("🧪 user_doc:", user_doc.to_dict())  # Debug print
        if not user_doc.exists:
            return f"❌ User {pro_id} not found", 404
        user_data = user_doc.to_dict() or {}
        nick = user_data.get("nick", "Unknown")

        # --- Fetch song ---
        song_doc = db.collection("songs").document(song_id).get()
        print("🧪 song_doc:", song_doc.to_dict())  # Debug print
        if not song_doc.exists:
            return f"❌ Song {song_id} not found", 404
        song_data = song_doc.to_dict() or {}
        song_name = song_data.get("name", "Unknown")

        # --- Write log entry ---
        db.collection("logs").add({
            "type": "rating",
            "proID": pro_id,
            "nick": nick,
            "songID": song_id,
            "songName": song_name,
            "rate": rate,
            "timestamp": datetime.now(timezone.utc),
            "source": "cloud_function"
        })

        return f"✅ Logged rating for {song_name} by {nick}: {rate} stars"

    except Exception as e:
        return f"🔥 Internal error: {str(e)}", 500
