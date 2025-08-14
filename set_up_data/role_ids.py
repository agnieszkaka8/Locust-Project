from set_up_data.endpoints_data import Endpoints

class UserRoles:
    global_admin = "Global Admin"
    manager = "Worker"
    customer = "Customer"

def get_roles_map(client):
    response = client.get(Endpoints.roles_path)
    if response.status_code == 200:
        roles = response.json()
        return {role["name"]: role["id"] for role in roles}
    return {}