from actions.base_actions import BaseUser
from locust import task
from set_up_data.endpoints_data import Endpoints
from set_up_data.role_ids import get_roles_map
from configs.config import get_admin_credentials
from faker import Faker
import random

fake = Faker()

class AdminUser(BaseUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roles_map = None

    def on_start(self):
        self.login()
        self.roles_map = get_roles_map(self.client)

    def login(self):
        creds = get_admin_credentials()
        self.client.post(Endpoints.login_path, creds)

    @task(3)
    def browse_all_products(self):
        self.get_web(Endpoints.products_path)

    @task(1)
    def add_user_worker(self):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = (f"{first_name.lower()}.{last_name.lower()}"
                 f"{random.randint(100, 999)}@quickshop.fake")

        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "role": self.roles_map.get("Worker"),
            "email": email
        }
        self.post_web(Endpoints.users_path, new_user)

    @task(4)
    def add_product(self):
        new_product = {
            "name": fake.word().capitalize() + " " + fake.word().capitalize(),
            "price": round(random.uniform(10.0, 500.0), 2)
        }
        response = self.post_web(Endpoints.products_path, new_product)
        new_product_id = response.json().get("id")

        updated_product = {
            "name": "EDITED" + fake.word().capitalize() + " " + fake.word().capitalize(),
            "price": round(random.uniform(10.0, 500.0), 2)
        }
        self.put_web(Endpoints.products_path, new_product_id, updated_product)
        self.delete_web(Endpoints.products_path, new_product_id)