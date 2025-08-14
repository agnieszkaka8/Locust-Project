import csv

from actions.base_actions import BaseUser
from locust import task
from set_up_data.endpoints_data import Endpoints
import random

def load_users(file_path="users.csv"):
    users = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append({"username": row["username"], "password": row["password"]})
    return users

USERS = load_users()

class AnonymousShopperUser(BaseUser):

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

    @task(1)
    def buy_product(self):
        if not self.products_list:
            return
        product_id = random.choice(self.products_list)
        order = {
            "product_id": product_id,
            "quantity": random.randint(1,3)
        }
        self.post_web(Endpoints.orders_path, order)

class LoggedInShopperUser(BaseUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products_list = []
        self.username = None
        self.password = None

    def on_start(self):
        user = random.choice(USERS)
        self.username = user["username"]
        self.password = user["password"]
        self.login(self.username, self.password)
        self.browse_all_products()

    def login(self, username, password):
        login_data = {"username": username, "password": password}
        self.client.post(Endpoints.login_path, json=login_data)

    @task(3)
    def browse_all_products(self):
        response = self.get_web(Endpoints.products_path)
        self.products_list = [p['id'] for p in response.json()]

    @task(3)
    def browse_product_detail(self):
        if self.products_list:
            product_id = random.choice(self.products_list)
            self.get_web(Endpoints.products_path, product_id)

    @task(1)
    def buy_product(self):
        if not self.products_list:
            return
        product_id = random.choice(self.products_list)
        order = {
            "product_id": product_id,
            "quantity": random.randint(1, 3)
        }
        self.post_web(Endpoints.orders_path, order)