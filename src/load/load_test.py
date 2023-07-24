from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between consecutive tasks, in seconds

    @task
    def hit_endpoint(self):
        self.client.get("http://staging.viberary.pizza")

    @task(2)
    def send_query(self):
        response = self.client.get("http://staging.viberary.pizza/search?query=scifi")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
