import json
import string
from random import choice

import requests


def main(api_url):
    """this function creates a user and an org and return the api key."""
    random_password = "".join(choice(string.ascii_letters + string.digits) for _ in range(8))

    register_response = requests.post(
        f"http://{api_url}:3000/v1/auth/register",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "firstName": "myem",
                "lastName": "dev",
                "email": "myem+dev@myem.fr",
                "password": random_password,
            }
        ),
    )

    access_token = register_response.json()["data"]["token"]

    requests.post(
        f"http://{api_url}:3000/v1/organizations",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
        data=json.dumps({"name": "myem"}),
    )

    login_response = requests.post(
        f"http://{api_url}:3000/v1/auth/login",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"email": "myem+dev@myem.fr", "password": random_password}),
    )

    access_token = login_response.json()["data"]["token"]

    api_key = requests.get(
        f"http://{api_url}:3000/v1/environments/api-keys",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
    ).json()["data"][0]["key"]

    print(api_key)
