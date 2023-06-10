# Bot Setup

Install the packages from the requirements.txt file in a python virtual enviroment by running pip3 install -r requirements.txt .

Use a .env file for your Discord Token, OpenAI API Key and CoinMarketCap API Key.

Run main.py 

# Bot Information

The bot uses the text-davinci-003, gpt-3.5-turbo, gpt-4 and image-alpha-001 models from OpenAI to generate responses and send them in text channels in discord. The Bot also uses CMC API to get the price and market capitalization of cryptocurrencies. 

# List of discord commands

?ask - insert a question and get an answer using the new gpt-4 model 

?fast - insert a question and get an answer using the new gpt-3.5-turbo model

?old - insert a question and get an answer using the text-davinci-003 model 

?recipe - insert ingredients separeted by commas and get a recipe 

?fact - insert a topic and get a fun fact 

?keypoints - insert a topic to highlight 5 keypoints about that topic 

?study - insert a topic and get study notes 

?image - generate image based on a description 

?joke - tell me a joke 

?roll - roll the dice 

?price - insert cryptocurrency symbol to get price and market cap

?collect - collects inserted text and stores it in the data.txt file locally

?showdata - shows the contets of the document mentioned previously 

?help - list of all commands
