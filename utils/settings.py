import os

from decouple import config

# Constants and Configuration
DISCORD_TOKEN = config("DISCORD_TOKEN")
OPENAI_API_KEY = config("OPENAI_API_KEY")
CMC_API_KEY = config("CMC_PRO_API_KEY")
CMC_API_URL = config("CMC_API_URL", default="https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest")
VISION_BRAIN_API_KEY = config("VISION_BRAIN_API_KEY", default="no-api-key-for-bot-to-start")
VISION_BRAIN_API_URL = config("VISION_BRAIN_API_URL", default="https://visionbrain.xyz/api/tts/")

OLLAMA_SERVER = config("OLLAMA_SERVER", default="http://localhost:11434")

IMAGE_FOLDER = config("IMAGE_FOLDER", default="generated_images")
os.makedirs(IMAGE_FOLDER, exist_ok=True)

DATA_FOLDER = config("DATA_FOLDER", default="data")
os.makedirs(DATA_FOLDER, exist_ok=True)

CHATS_FOLDER = config("CHATS_FOLDER", default=os.path.join(DATA_FOLDER, "chats"))
os.makedirs(CHATS_FOLDER, exist_ok=True)

RECIPES_FILE = os.path.join(DATA_FOLDER, "recipes.json")
COMPLETIONS_FILE = os.path.join(DATA_FOLDER, "completions.json")
CLASSIFICATIONS_FILE = os.path.join(DATA_FOLDER, "classifications.json")
