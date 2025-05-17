from google.cloud import firestore

def log_rating(request):
    request_json = request.get_json(silent=True)
    db = firestore.Client()

    if request_json and 'song' in request_json and 'rating' in request_json:
        log_data = {
            'song': request_json['song'],
            'rating': request_json['rating']
        }
        db.collection('logs').add(log_data)
        return f"Logged rating for {request_json['song']}", 200
    else:
        return "Missing song or rating", 400
