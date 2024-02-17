from locust import HttpUser, task, between
import random


class MyUser(HttpUser):
    wait_time = between(1, 5)

    phone_numbers = [
        '09172101171', '09172101172', '09172101173', '09172101174', '09172101175',
        '09172101176', '09172101177', '09172101178', '09172101179', '09172101180',
        '09172101181', '09172101182', '09172101183', '09172101184', '09172101185',
    ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credit = 0
        self.phone_number = random.choice(self.phone_numbers)
        self.phone_numbers.remove(self.phone_number)

    def on_start(self):
        url = "http://127.0.0.1:8000/addcostumer/"
        data = {
            "phone_number": self.phone_number,
            "credit": self.credit
        }
        response = self.client.post(url, json=data)
        try:
            print(response.json())
            print(self.phone_number)
        except Exception as e:
            print(e)

    @task
    def nothing_else(self):
        pass
