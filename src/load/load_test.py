from locust import HttpUser, task


class MyUser(HttpUser):

    @task(1)
    def send_query(self):
        response = self.client.get("http://staging.viberary.pizza/search?query=scifi")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
