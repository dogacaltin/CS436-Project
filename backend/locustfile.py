from locust import HttpUser, task, between
import random

class CloudRateUser(HttpUser):
    wait_time = between(1, 3)

    song_ids = [
        "6QAsrXPnMSXIbV0yEJHlEX",  
        "02xhLoVqpGmOqvolgrwM8w",
        "03sf6gnuqZNE9sGrRi8WAc",
        "0DuWDLjriRPjDRoPgaCslY",
        "0Z5ok0QLLttAKsujOZYOXf",
        "0x9154bA7PgqF6Za1CtszP"
 
        
    ]

    pro_ids = [
        "c9afae1b-af9b-42ac-a444-b396b8a97048",
        "vti0xCOqdcqLOuPg55QU",
        "53daf917-7b51-4228-9996-1ce2e183e140",
        "61f1367d-0ddd-4ade-970f-9fbbe6f4a784",
        "6571429d-7e6d-4c70-9a4f-66b04bec96b8",
        "7a008a27-af1c-4463-9306-1da8e60c6e8f"
    ]

    @task(3)
    def search_song(self):
        query = random.choice(["Chasing", "Else", "Love", "One","Unuttun"])
        self.client.get("/search", params={"query": query, "type": "song"})

    @task(2)
    def rate_song(self):
        payload = {
            "songID": random.choice(self.song_ids),
            "proID": random.choice(self.pro_ids),
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
