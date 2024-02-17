from locust import HttpUser, task, between
import random


class MyUser(HttpUser):
    wait_time = between(1, 5)

    usernames = [
        "Liam"
    ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credit = round(random.uniform(10000, 20000), 10)
        self.username = random.choice(self.usernames)
        self.usernames.remove(self.username)

    def on_start(self):
        url = "http://127.0.0.1:8000/addseller/"
        data = {
            "username": self.username,
            "credit": self.credit
        }
        response = self.client.post(url, json=data)
        try:
            print(response.json())
            print(self.username)
        except Exception as e:
            print(e)

    @task
    def nothing_else(self):
        pass
