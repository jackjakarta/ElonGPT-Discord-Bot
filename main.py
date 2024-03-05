import discord

from app.commands import ask_command, fast_command, imagine_command, recipe_command
from app.commands import price_command, joke_command, poll_command, help_command, classify_command
from utils.settings import DISCORD_TOKEN

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    activity = discord.Activity(name="?help", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    guild_count = len(client.guilds)
    print(f"{client.user} has connected to Discord!")
    print(f"{client.user} is active on {guild_count} server(s).")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("?ask"):
        await ask_command(message)
    elif message.content.startswith("?fast"):
        await fast_command(message)
    elif message.content.startswith("?image"):
        await imagine_command(message)
    elif message.content.startswith("?recipe"):
        await recipe_command(message)
    elif message.content.startswith("?classify"):
        await classify_command(message)
    elif message.content.startswith("?price"):
        await price_command(message)
    elif message.content.startswith("?poll"):
        await poll_command(message)
    elif message.content.startswith("?joke"):
        await joke_command(message)
    elif message.content.startswith("?help"):
        await help_command(message)


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
