from random import choice

import requests
from httpx import ConnectError

from app.ai.chat import ChatGPT, ImageClassify, Ollama
from app.ai.imagine import ImageDallE
from utils import save_json, load_json, create_embed, check_moderate
from utils.settings import CLASSIFICATIONS_FILE, COMPLETIONS_FILE, RECIPES_FILE
from utils.settings import CMC_API_KEY, CMC_API_URL, VISION_BRAIN_API_KEY, VISION_BRAIN_API_URL


# Text Generation Commands
async def ask_command(message):
    await message.channel.send(f"***Elon is cooking for {message.author.name}***")

    try:
        ai = ChatGPT()
        prompt = message.content[5:]
        answer = ai.ask(prompt)

        await message.channel.send(f"***Answer for {message.author.name}:***\n\n{answer}")

        # Save to JSON
        json_data = load_json(COMPLETIONS_FILE)
        json_data.append(
            {
                "user": message.author.name,
                "prompt": prompt,
                "completion": answer,
            }
        )
        save_json(COMPLETIONS_FILE, json_data)
        print("Prompt - Completion Pair saved to completions.json file!")

    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Error: {e}")


async def fast_command(message):
    await message.channel.send(f"***Elon is cooking for {message.author.name}***")

    prompt = message.content[6:]
    try:
        if check_moderate(prompt):
            await message.channel.send("***Prompt is not appropriate and contains harmful content***")
        else:
            ai = ChatGPT(model="gpt-4o-mini")
            answer = ai.ask(prompt)

            await message.channel.send(f"***Answer for {message.author.name}:***\n\n{answer}")

            json_data = load_json(COMPLETIONS_FILE)
            json_data.append(
                {
                    "user": message.author.name,
                    "prompt": prompt,
                    "completion": answer,
                }
            )
            save_json(COMPLETIONS_FILE, json_data)
            print("Prompt - Completion Pair saved to completions.json file!")

    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Error: {e}")


async def ollama_command(message):
    await message.channel.send(f"***Elon is cooking for {message.author.name}***")

    try:
        ai = Ollama()

        prompt = message.content[8:]
        response = ai.ask(prompt)
        await message.channel.send(f"***Answer for {message.author.name}:***\n\n{response}")

    except ConnectError as e:
        description = f"Connection to Model failed. Error: {e}"
        embed = create_embed(title="Model Connection Error:", description=description)
        await message.channel.send(embed=embed)


async def recipe_command(message):
    await message.channel.send(f"***Elon is cooking for {message.author.name}***")

    try:
        ingredients = message.content[8:]
        prompt = f"Write a recipe based on these ingredients:\n{ingredients}\n"

        ai = ChatGPT()
        recipe = ai.ask(prompt)

        await message.channel.send(f"***Recipe for {message.author.name}:***\n\n{recipe}")

        recipes_data = load_json(RECIPES_FILE)
        recipes_data.append(
            {
                "user": message.author.name,
                "ingredients": ingredients,
                "recipe": recipe,
            }
        )
        save_json(RECIPES_FILE, recipes_data)

    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")

async def get_recipes_command(message):
    try:
        # Load all recipes from the JSON file
        recipes_data = load_json(RECIPES_FILE)

        # Filter recipes by the user who requested them
        user_recipes = [recipe for recipe in recipes_data if recipe["user"] == message.author.name]

        if not user_recipes:
            await message.channel.send(f"***{message.author.name}, you have no saved recipes yet.***")
            return

        # Prepare a string to display the user's recipes
        recipes_message = f"***Recipes for {message.author.name}:***\n\n"
        messages_to_send = []
        
        for idx, recipe in enumerate(user_recipes, start=1):
            recipe_text = f"**Recipe {idx}:**\nIngredients: {recipe['ingredients']}\nRecipe: {recipe['recipe']}\n\n"
            
            # Check if the current message is too long, if so, split it
            if len(recipes_message) + len(recipe_text) > 2000:
                messages_to_send.append(recipes_message)
                recipes_message = ""  # Start a new message chunk
            
            recipes_message += recipe_text
        
        # Append any remaining message to the list
        if recipes_message:
            messages_to_send.append(recipes_message)

        # Send each message separately
        for msg in messages_to_send:
            await message.channel.send(msg)

    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=str(e))
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")



async def chat_command(message):
    try:
        prompt = message.content[6:]
        ai = ChatGPT(user_name=message.author.name)

        if prompt and prompt != "clear":
            await message.author.send(ai.ask(prompt))
            ai.save_chat()

        elif prompt == "clear":
            ai.delete_chat()
            await message.author.send("***Chat reset successfully!***")

        else:
            responses = [
                f"Hello {message.author.name}, use ***?chat your question here*** to chat with the bot or  "
                "***?chat clear*** to reset the conversation. Use ***?help*** to see all commands.",

                f"Hey there, {message.author.name}! Feel free to interact with me by typing ***?chat your question "
                "here***. Need a fresh start? Just type ***?chat clear***. For a list of all commands, type "
                "***?help***.",

                f"Greetings, {message.author.name}! Use ***?chat your question*** here to start a conversation with "
                "me, or type ***?chat clear*** if you want to begin anew. Curious about what else I can do? Type "
                "***?help*** for a full list of commands.",

                f"Hi {message.author.name}! To chat with me, type ***?chat your question here***. Want to clear our "
                "conversation? Just enter ***?chat clear***. If you need assistance or want to explore more commands, "
                "type ***?help***."
            ]
            await message.channel.send("***Check your DMs***")
            await message.author.send(choice(responses))

    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


# Image Commands
async def imagine_command(message):
    await message.channel.send(f"***Elon is cooking for {message.author.name}***")

    try:
        ai = ImageDallE()
        prompt = message.content[7:]
        ai.generate_image(prompt)

        await message.channel.send(ai.image_url)
        ai.save_image()
        print(f"Image for {message.author.name} saved to {ai.image_path}.")

    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


async def classify_command(message):
    await message.channel.send(f"***Elon is cooking for {message.author.name}***")
    input_url = message.content[10:]

    try:
        ai = ImageClassify()
        answer = ai.classify_image(input_url)

        await message.channel.send(f"***Image Classification for {message.author.name}:***\n\n{answer}")

        classification = {
            "user": message.author.name,
            "url": input_url,
            "classification": answer,
        }

        json_data = load_json(CLASSIFICATIONS_FILE)
        json_data.append(classification)
        save_json(CLASSIFICATIONS_FILE, json_data)
        print(f"Image classification saved to {CLASSIFICATIONS_FILE}.")

    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


# API Calls Commands
async def price_command(message):
    parts = message.content.split(" ")
    symbol = parts[1].upper()

    params = {
        "symbol": symbol,
        "convert": "USD",
        "CMC_PRO_API_KEY": CMC_API_KEY
    }
    response = requests.get(CMC_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        price = data["data"][symbol]["quote"]["USD"]["price"]
        market_cap = data["data"][symbol]["quote"]["USD"]["market_cap"]
        api_response = f"**Price:** ${price:.2f}\n**Market Cap:** ${market_cap:.2f}"
        embed = create_embed(title=symbol, description=api_response)

        await message.channel.send(embed=embed)
    else:
        await message.channel.send(f"Could not get price and market capitalization for {symbol}")


async def tts_command(message):
    await message.channel.send(f"***Generating audio for {message.author.name}***")
    text = message.content[5:]
    text_list = text.split("-v ")

    headers = {
        "X-Api-Key": VISION_BRAIN_API_KEY,
    }
    data = {
        "text": text_list[0] if len(text_list) > 1 else text,
        "voice": text_list[1] if len(text_list) > 1 else "fable",
    }

    try:
        response = requests.post(VISION_BRAIN_API_URL, data=data, headers=headers)
        response.raise_for_status()
        data = response.json()
        md_encode = f"[Download File]({data.get('file')})"

        await message.channel.send(f"***Audio for {message.author.name}:***\n\n***File:*** {md_encode}\n"
                                   f"***Text:*** {data.get('text')}")

    except requests.exceptions.RequestException as e:
        await message.channel.send(f'An error occurred: {e}')
        print(f'An error occurred: {e}')
    else:
        print('API call was successful!')
        print(f"API Call by {message.author.name} - {data}")


async def joke_command(message):
    category = message.content[6:]

    # Get and format joke categories
    categories_url = "https://api.chucknorris.io/jokes/categories"
    get_categories = requests.get(categories_url)
    get_categories_list = get_categories.json()
    categories = ", ".join(get_categories_list)

    if category not in get_categories_list:
        await message.channel.send(f"**Available categories:** {categories}")
    else:
        try:
            joke_url = f"https://api.chucknorris.io/jokes/random?category={category}"
            api_response = requests.get(joke_url)

            if api_response.status_code == 200:
                joke = api_response.json()
                joke_format = joke.get("value")
                await message.channel.send(joke_format)
            else:
                embed = create_embed(title="API Call Failed:", description="Could not retrieve joke from Chuck Norris "
                                                                           "API.")
                await message.channel.send(embed=embed)
        except Exception as e:
            embed = create_embed(title="API Call Error:", description=e)
            await message.channel.send(embed=embed)
            print(f"API Call Error: {e}")


# Own Commands
async def poll_command(message):
    await message.channel.send(f"***Creating poll for {message.author.name}***")

    poll_data = message.content[6:].split('/')
    question = poll_data[0].strip()
    options = [option.strip() for option in poll_data[1:]]

    embed = create_embed(title=question, description=None)

    for i, option in enumerate(options):
        embed.add_field(name=f"{i + 1}. {option}", value="\u200b", inline=False)

    poll_message = await message.channel.send(embed=embed)

    for i in range(len(options)):
        await poll_message.add_reaction(f'{i + 1}\u20e3')


async def help_command(message):
    help_text = "***?ask*** - insert a question and get an answer from Elon (gpt-4) \n\n" \
                "***?fast*** - insert a question and get an answer in fast mode (gpt-3.5) \n\n" \
                "***?chat*** - open chat session and then use ?chat 'prompt' to chat with Elon \n\n" \
                "***?ollama*** -  insert a question and get an answer from your selected model (default = orca-mini\n\n" \
                "***?recipe*** - insert ingredients and get a recipe \n\n" \
                "***?myrecipes*** - get your recipes \n\n" \
                "***?image*** - insert prompt to generate an image based on a description \n\n" \
                "***?classify*** - insert image url to generate an image description \n\n" \
                "***?price*** - insert cryptocurrency symbol to get price and market cap \n\n" \
                "***?joke*** - insert category to get chuck norris joke \n\n" \
                "***?poll*** - example: ?poll what color?/blue/red/yellow \n\n" \
                "***?help*** - list of all commands \n"

    embed = create_embed(title="list of commands:", description=help_text)
    await message.channel.send(embed=embed)
