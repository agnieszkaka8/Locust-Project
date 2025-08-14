from actions.base_actions import BaseUser
from locust import task
from set_up_data.endpoints_data import Endpoints
import random

class GuestUser(BaseUser):

    def __init__(self):
        super().__init__()
        self.products_list = []

    @task(3)
    def browse_all_products(self):
        response = self.get_web(Endpoints.products_path)
        self.products_list = [p['id'] for p in response.json()]

    @task(3)
    def browse_product_detail(self):
        if self.products_list:
            product_id = random.choice(self.products_list)
            self.get_web(Endpoints.products_path, product_id)
