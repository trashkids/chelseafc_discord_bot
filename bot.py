#!/usr/bin/python

import logging
import os
import discord
from dotenv import load_dotenv
import openai

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv('OPENAI_API_KEY')

# GPT3にテキストを送り回答を返す関数
def generate_answer(text):
    prompt = (f'{text}とは何ですか？')
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      temperature=0.5,
      max_tokens=50,
      n=1,
      stop=None,
      timeout=10,
    )
    answer = response.choices[0].text.strip()
    return answer

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('こんにちは'):
        await message.channel.send('こんにちは')

    # メンションを含むメッセージを処理する
    if client.user in message.mentions:
        text = message.content.replace(f'<@!{client.user.id}>', '')
        text = text.replace('　', ' ').strip()
        answer = generate_answer(text)
        await message.channel.send(answer)

# 環境変数を読み込む部分の修正
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)