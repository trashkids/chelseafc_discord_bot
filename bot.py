import os
import discord
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 追加した部分
    if message.channel.name != 'test':
        return

    if message.content.startswith('こんにちは'):
        await message.channel.send('こんにちは')

# 環境変数を読み込む部分の修正
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)