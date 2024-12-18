# Discord Bot with AI Integration

**Table of Contents**

- [Introduction](#introduction)
- [Features](#features)
- [Bot Setup](#bot-setup)
- [Docker Run](#docker-run)
- [Discord Commands](#discord-commands)

## Introduction

This bot seamlessly integrates with a variety of AI models to offer engaging and practical features. It leverages the OpenAI API for natural language processing tasks and harnesses the power of DALL-E for image generation. Additionally, it can interact with the CoinMarketCap API to provide up-to-date cryptocurrency data. Please note that this bot uses the older Discord library for bot creation and does not employ application commands.

## Branch

Use the `release/v1` branch to run the bot. The `main` branch has been updated with some personal configuration.

## Features

Explore the exciting features of this Discord bot:

### Question Answering

Use the `?ask` command to ask questions and receive responses from the advanced gpt-4 model.

### Image Generation

Create images based on descriptions by using the `?image` command, which utilizes the DALL-E 3 model.

### Image Classification

Classifies images by using the `?classify` command, using the new GPT-4 vision model.

### Cryptocurrency Price

Stay informed about cryptocurrency prices and market capitalization by executing the `?price` command.

### Polls

Engage your server members by creating polls with multiple options using the `?poll` command.

## Bot Setup

To set up this bot on your own server, follow these steps:

1. Clone this repository to your local machine.

2. Consider creating a virtual environment (recommended but optional).

3. Install the necessary dependencies by running the following command:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Configure your environment variables following the template provided at `.env.default`.

5. Start the bot by executing the following command:

   ```bash
   python3 main.py
   ```

6. Or, start the bot in the background by executing the start script labeled `start_bot.sh`.

   ```bash
   ./start_bot.sh
   ```

## Docker

Alternatively, you can run the bot within a Docker container.

### Run container

Run the container while supplying your environment variables. (remember to use the right branch)

```bash
docker build -t yourimagename:tag .
```

```bash
docker run -d -t \
-e OPENAI_API_KEY=your-api-key \
-e DISCORD_TOKEN=your-api-key \
-e CMC_PRO_API_KEY=your-api-key \
--name elongpt-bot \
yourimagename:tag
```

You can access the container's bash shell with.

```bash
docker exec -it elongpt-bot bash
```

## Discord Commands

Now that your bot is up and running, here are some of the commands you can use:

- `?help`: Retrieve a list of all available commands.

- `?ask 'question'`: Ask a question and receive an answer from the gpt-4 model.

- `?fast 'question'`: Get a quick answer using the gpt-3.5-turbo model.

- `?ollama 'question'`: Get an answer using ollama from your hosted model.

- `?chat`: open chat session in DMs and then use `?chat 'prompt'` to chat with the bot.

- `?image 'description'`: Generate an image based on a description.

- `?classify 'image url'`: Classifies images and describes them

- `?price 'symbol'`: Fetch the price and market cap of a cryptocurrency.

- `?joke`: Enjoy a Chuck Norris joke using the free API.

- `?poll 'question'/'option1'/'option2'/...`: Create a poll with multiple options and engage your server members in a vote.
