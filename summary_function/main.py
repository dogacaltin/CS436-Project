from google.cloud import firestore
from datetime import datetime, timezone
import functions_framework

@functions_framework.cloud_event
def generate_daily_summary(_):
    db = firestore.Client()
    logs_ref = db.collection("logs")
    logs = [doc.to_dict() for doc in logs_ref.stream()]

    now = datetime.now(timezone.utc)
    today = now.date()

    total_count = len(logs)

    db.collection("daily_summary").document(str(today)).set({
        "date": str(today),
        "totalCount": total_count,
        "updatedAt": now
    })

    print(f"✅ Saved summary: totalCount = {total_count}")
