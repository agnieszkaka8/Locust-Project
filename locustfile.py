from locust import HttpUser, between, task
from users.shopper_user import AnonymousShopperUser, LoggedInShopperUser

class AnonymousShopperLocust(AnonymousShopperUser):
    wait_time = between(1, 3)

class LoggedInShopperLocust(LoggedInShopperUser):
    wait_time = between(1, 3)

