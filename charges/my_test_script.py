from locust import HttpUser, task, between
import random


class MyUser(HttpUser):
    wait_time = between(1, 5)

    usernames = [
        "Liam"
    ]

    phone_numbers = [
        '09172101171', '09172101172', '09172101173', '09172101174', '09172101175',
        '09172101176', '09172101177', '09172101178', '09172101179', '09172101180',
        '09172101181', '09172101182', '09172101183', '09172101184', '09172101185',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phone_number = random.choice(self.phone_numbers)
        self.username = random.choice(self.usernames)

    @task
    def inner_charge(self):
        url = "http://127.0.0.1:8000/sellerincrease/"
        data = {
            "username": self.username,
            "amount": round(random.uniform(100, 1000), 10)
        }
        response = self.client.put(url, json=data)
        try:
            print(response.json())
            print(self.username)
        except Exception as e:
            pass

    @task(5)
    def transact(self):
        url = "http://127.0.0.1:8000/sell/"
        data = {
            "username": self.username,
            "phone_number": self.phone_number,
            "amount": round(random.uniform(100, 1000), 10)
        }
        response = self.client.put(url, json=data)
        try:
            print(response.json())
            print(self.username)
        except Exception as e:
            pass
