import openai
import discord
import os


# Load the API key and Discord Token from the .env file
TOKEN = os.environ['DISCORD_TOKEN']
openai.api_key = os.environ['OPENAI_API_KEY']

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    activity = discord.Activity(name='use | ?help', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    if message.content.startswith("?ask"):
        question = message.content[5:]
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(f"{question}"),
            max_tokens=250,
            n = 1,
            stop=None,
            temperature=0.9,
        )
        await message.channel.send(response["choices"][0]["text"])

        
    if message.content.startswith("?recipe"):
        ingredients = message.content[8:]
        prompt = f"Write a recipe based on these ingredients:\n\n{ingredients}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.3,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])
    
  
    if message.content.startswith("?fact"):
        topic = message.content[4:]
        prompt = f"Tell me a fun fact about:\n\n{topic}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])

        
    if message.content.startswith("?keypoints"):
        subject = message.content[4:]
        prompt = f"Highlight 5 keypoints about:\n\n{subject}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=350,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])   

        
    if message.content.startswith("?study"):
        studytopic = message.content[4:]
        prompt = f"What are 5 key points I should know when studying:\n\n{studytopic}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.4,
            max_tokens=400,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])  


    if message.content.startswith("?joke"):
        prompt = "Tell me a joke"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])

  
    if message.content.startswith("?roll"):
        prompt = "Roll the dice"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])
  
  
    if message.content.startswith("?help"):
        help_text = "?ask - insert a question and get an answer \n" \
                    "?recipe - insert ingredients separeted by commas and get a recipe \n"\
                    "?fact - insert a topic and get a fun fact \n"\
                    "?keypoints - insert a topic to highlight 5 keypoints about that topic \n"\
                    "?study - insert a topic and get study notes \n"\
                    "?image - generate image based on a description \n"\
                    "?joke - tell me a joke \n"\
                    "?roll - roll the dice \n"\
                    "?help - list of all commands \n"
            
        embed = discord.Embed(title="list of commands:", description=help_text, color=0x4BA081)
        await message.channel.send(embed=embed)


    if message.content.startswith("?image"):
        # Get the text input
        text = message.content[6:]

        # Generate an image using the Dall-E model
        prompt=f"Generate an image based on the following description:\n\n{text}"
        response = openai.Image.create(
            model="image-alpha-001",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Get the URL of the generated image
        image_url = response['data'][0]['url']

        # Send the URL as a message in Discord
        await message.channel.send(image_url)


client.run(TOKEN)
