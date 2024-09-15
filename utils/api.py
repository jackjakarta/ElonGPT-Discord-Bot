import requests

from .settings import BACKEND_API_URL


def db_create_recipe(discord_user: str, ingredients: str, instructions: str):
    try:
        url = f"{BACKEND_API_URL}/recipes"

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "discordUser": discord_user,
            "ingredients": ingredients,
            "instructions": instructions,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()
    
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"


def db_create_completion(discord_user: str, prompt: str, completion: str):
    try:
        url = f"{BACKEND_API_URL}/completion"

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "discordUser": discord_user,
            "prompt": prompt,
            "completion": completion,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()
    
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"

def db_create_classification(discord_user: str, image_url: str, classification: str):
    try:
        url = f"{BACKEND_API_URL}/classification"

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "discordUser": discord_user,
            "imageUrl": image_url,
            "classification": classification,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()
    
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"