import logging

# ロガーを作成する
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ログをファイルに出力するハンドラを作成する
log_file = '../discord_bot.log'
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# ログのフォーマットを設定する
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)

# ロガーにハンドラを追加する
logger.addHandler(file_handler)


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