from locust import HttpUser, task


class TestUser(HttpUser):
    @task
    def main(self):
        self.client.get("/")
