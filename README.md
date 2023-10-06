# Discord Bot with AI Integration

This is a Discord bot that integrates with various AI models to provide fun and useful features. It uses the OpenAI API for natural language processing tasks and image generation with DALL-E. It also interacts with the CoinMarketCap API for cryptocurrency data retrieval.
 
# Features

Question Answering: Ask questions using the ?ask command and receive answers from the gpt-4 model.

Image Generation: Generate images based on descriptions using the DALL-E model with the ?image command.

Cryptocurrency Price: Get the price and market capitalization of a cryptocurrency using the ?price command.

Polls: Create polls with multiple options using the ?poll command.

# Bot Setup

Clone this repository to your local machine.

Create a virtual environment (optional but recommended).

Install the required dependencies using pip3 install -r requirements.txt.

Set up environment variables for your Discord bot token, OpenAI API key, and CoinMarketCap API key in a .env file.

Run the bot using python3 main.py.

# Discord Commands

?help - Get a list of all available commands.

?ask 'question' - Ask a question and get an answer from the gpt-4 model.

?fast 'question' - Get a quick answer using the gpt-3.5-turbo model.

?image 'description' - Generate an image based on a description.

?price 'symbol' - Get the price and market cap of a cryptocurrency.

?poll 'question'/'option1'/'option2'/... - Create a poll with options.
