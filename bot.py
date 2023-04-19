#!/usr/bin/python

import logging
import os
import discord
import re
from dotenv import load_dotenv
import openai

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv('OPENAI_API_KEY')

# GPT3にテキストを送り回答を返す関数
def generate_answer(text):
    prompt = f"ユーザーが次のように言っています: '{text}'。これに対する適切な返答は何ですか？"
    response = openai.Completion.create(
#      engine="text-davinci-003",
      engine="gpt-4",
      prompt=prompt,
      temperature=0.5,
      max_tokens=2000,
      n=1,
      timeout=10,
)

    answer = response.choices[0].text.strip()
    return answer

# 日本語判定をする関数
def is_japanese(text):
    regex = r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf]+'
    return bool(re.search(regex, text))

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()

    if not is_japanese(text):
        return

    logger.info(f"User input: {text}")
    answer = generate_answer(text)
    logger.info(f"API response: {answer}")

    await message.channel.send(answer)
    logger.info(f"Bot sent message: {answer}")

# 環境変数を読み込む部分の修正
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)