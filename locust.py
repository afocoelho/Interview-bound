from locust import HttpLocust, TaskSet, between



class UserBehavior(TaskSet):

    @task(1)
    def track(self):
        self.client.post("track",json =  {"userId": "fakeid01","events": [{"eventName": "test","metadata": {"test":1},"timestampUTC": 0}]})
    @task(2)
    def alias(self):
        self.client.post("alias",  json = {  "newUserId": 'user02',"originalUserId": 'user01',"timestampUTC": 0})
    @task(3)
    def profile(self):
        self.client.post("profile",json = {   "userId": "string",  "attributes": {},  "timestampUTC": 0 })
    @task(4)
    def index(self):
        self.client.get("/")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
