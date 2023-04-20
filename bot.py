#!/usr/bin/python

import logging
import os
import discord
import re
import json
import requests
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_url = os.getenv('OPENAI_API_URL') or 'https://api.openai.com/v1/chat/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai_api_key}',
}

# Function to send text to GPT-4 and return the answer
def generate_answer(text):
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'あなたは若者で、カジュアルな話し方をします。敬語を使わずスラングを使います。'},
            {'role': 'user', 'content': text}
        ],
        'temperature': 0.8,
        'max_tokens': 500,
        'n': 1,
    }
    
    response = requests.post(openai_api_url, headers=headers, json=data)
    response_json = response.json()
    
    if response.status_code == 200:
        answer = response_json['choices'][0]['message']['content'].strip()
        return answer
    else:
        logger.error(f"API error: {response_json}")
        return "Error: Unable to generate a response."

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the bot is mentioned in the message
    if client.user.mentioned_in(message):
        text = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()

        logger.info(f"User input: {text}")
        answer = generate_answer(text)
        logger.info(f"API response: {answer}")

        await message.channel.send(answer)
        logger.info(f"Bot sent message: {answer}")
    else:
        # Do nothing if the bot is not mentioned
        return

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)