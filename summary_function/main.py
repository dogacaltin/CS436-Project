from google.cloud import firestore
from datetime import datetime, timezone
import functions_framework

@functions_framework.cloud_event
def generate_daily_summary(cloud_event):
    db = firestore.Client()
    logs_ref = db.collection("logs")
    logs = [doc.to_dict() for doc in logs_ref.stream()]

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    daily_count = sum(
        1 for log in logs
        if "timestamp" in log and log["timestamp"].astimezone(timezone.utc).strftime("%Y-%m-%d") == today_str
    )

    total_count = len(logs)

    db.collection("daily_summary").document(today_str).set({
        "date": today_str,
        "dailyCount": daily_count,
        "totalCount": total_count,
        "updatedAt": now
    })

    print(f"✅ Saved summary: {daily_count} today, {total_count} total")
