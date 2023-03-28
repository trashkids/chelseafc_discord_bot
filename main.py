import discord
import pytz
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
DISCORD_CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
FOOTBALL_DATA_TEAM_ID = int(os.environ['FOOTBALL_DATA_TEAM_ID'])
FOOTBALL_DATA_API_KEY = os.environ['FOOTBALL_DATA_API_KEY']
TIMEZONE = os.environ['Asia/Tokyo']

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

async def send_match_notification():
    url = f'http://api.football-data.org/v2/teams/{FOOTBALL_DATA_TEAM_ID}/matches?status=SCHEDULED'
    headers = {'X-Auth-Token': FOOTBALL_DATA_API_KEY}
    response = requests.get(url, headers=headers)
    matches = response.json()['matches']
    for match in matches:
        match_date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        tz = pytz.timezone(TIMEZONE)
        match_date = tz.normalize(match_date.astimezone(tz))
        current_date = datetime.now(tz)
        if current_date + timedelta(hours=1) == match_date:
            message = 'チェルシーFCの試合が1時間後に開始されます！'
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            await channel.send(message)

client.loop.create_task(send_match_notification())
client.run(DISCORD_BOT_TOKEN)