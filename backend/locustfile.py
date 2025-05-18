from locust import HttpUser, task, between
import random

class CloudRateUser(HttpUser):
    wait_time = between(1, 3)

    song_id = "6QAsrXPnMSXIbV0yEJHlEX"
    pro_id = "c9afae1b-af9b-42ac-a444-b396b8a97048"

    @task(3)
    def search_song(self):
        self.client.get("/search", params={"query": "Nothing Else", "type": "song"})

    @task(2)
    def rate_song(self):
        payload = {
            "songID": self.song_id,
            "proID": self.pro_id,
            "rate": round(random.uniform(1, 5), 1)
        }
        with self.client.post("/rate", json=payload, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"{response.status_code}: {response.text}")
            else:
                response.success()

    @task(1)
    def get_logs(self):
        self.client.get("/logs/random")
