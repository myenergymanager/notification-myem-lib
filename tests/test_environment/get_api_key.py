import json
import os

import requests


def main():
    """this function creates a user and an org and return the api key."""
    api_url = os.environ["API_URL"]
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_PASSWORD"]

    register_response = requests.post(
        f"{api_url}/v1/auth/register",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "firstName": "myem",
                "lastName": "dev",
                "email": email,
                "password": password,
            }
        ),
    )

    access_token = register_response.json()["data"]["token"]

    requests.post(
        f"{api_url}/v1/organizations",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
        data=json.dumps({"name": "myem"}),
    )

    login_response = requests.post(
        f"{api_url}/v1/auth/login",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"email": email, "password": password}),
    )

    access_token = login_response.json()["data"]["token"]

    api_key = requests.get(
        f"{api_url}/v1/environments/api-keys",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
    ).json()["data"][0]["key"]

    print(api_key)


if __name__ == "__main__":
    main()
