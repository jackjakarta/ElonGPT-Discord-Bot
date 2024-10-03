import requests

from .settings import BACKEND_API_URL, BACKEND_API_KEY


def get_endpoint(endpoint: str) -> str:
    return f"{BACKEND_API_URL}/{endpoint}"


def get_headers() -> dict:
    headers = {
        "Authorization": f"Bearer {BACKEND_API_KEY}",
        "Content-Type": "application/json",
    }

    return headers


def db_create_recipe(discord_user: str, ingredients: str, instructions: str):
    endpoint_url = get_endpoint("recipes")
    headers = get_headers()

    data = {
        "discordUser": discord_user,
        "ingredients": ingredients,
        "instructions": instructions,
    }

    response = requests.post(url=endpoint_url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()
    

def db_create_completion(discord_user: str, prompt: str, completion: str):
    endpoint_url = get_endpoint("completion")
    headers = get_headers()

    data = {
        "discordUser": discord_user,
        "prompt": prompt,
        "completion": completion,
    }

    response = requests.post(url=endpoint_url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()
    

def db_create_classification(discord_user: str, image_url: str, classification: str):
    endpoint_url = get_endpoint("classification")
    headers = get_headers()

    data = {
        "discordUser": discord_user,
        "imageUrl": image_url,
        "classification": classification,
    }

    response = requests.post(url=endpoint_url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()


def s3_save_image(discord_user: str, image_url: str, prompt: str):
    endpoint_url = get_endpoint("images")
    headers = get_headers()

    data = {
        "imageUrl": image_url,
        "discordUser": discord_user,
        "prompt": prompt,
    }

    response = requests.post(url=endpoint_url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()

def db_get_user_images(discord_user: str):
    endpoint_url = get_endpoint(f"images")
    query_endpoint = f"{endpoint_url}?discordUser={discord_user}"
    headers = get_headers()

    response = requests.get(url=query_endpoint, headers=headers)
    response.raise_for_status()

    return response.json()
