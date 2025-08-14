import os

environments = {
    "staging": {
        "host_url": "https://staging-api.quickshop.fake"
    },
    "dev": {
        "host_url": "https://dev-api.quickshop.fake"
    },
    "prod": {
        "host_url": "https://api.quickshop.fake"
    }
}

def get_environment():
    env = os.getenv("ENVIRONMENT")
    app_env = environments.get(env)
    print(f"Tests will be run against {env} environment ({app_env['host_url']}")
    return app_env

def get_admin_credentials():
    login = os.getenv("USER_ADMIN")
    password = os.getenv("PASSWORD_ADMIN")
    return {
        "username":login ,
        "password": password
    }