import abc

from locust import HttpUser, between
from configs.config import get_environment

class BaseUser(HttpUser):
    wait_time = between(1, 3)
    host = get_environment().get("host_url")

    def on_start(self):
        self.client.verify = False
        self.login()

    def login(self, *args):
        pass

    def get_web(self, path, item_id=None):
        if item_id is None:
            final_path = path
        else:
            final_path = f'{path}/{item_id}'
        return self.client.get(final_path)

    def post_web(self, path, data):
        self.client.post(path, json=data)

    def put_web(self, path, item_id, data):
        self.client.put(f'{path}/{item_id}', json=data)

    def delete_web(self, path, item_id):
        self.client.delete(f'{path}/{item_id}')