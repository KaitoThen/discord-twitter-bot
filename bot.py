import discord
import snscrape.modules.twitter as sntwitter
import asyncio
import os

TOKEN = os.getenv("TOKEN")  # Get bot token from Railway variables
CHANNEL_ID = 123456789  # Replace with your Discord channel ID
USERNAME = "elonmusk"  # Replace with the Twitter username

intents = discord.Intents.default()
client = discord.Client(intents=intents)
last_tweet_id = None

async def fetch_tweets():
    global last_tweet_id
    tweets = list(sntwitter.TwitterUserScraper(USERNAME).get_items())

    if tweets:
        latest_tweet = tweets[0]
        if last_tweet_id != latest_tweet.id:
            last_tweet_id = latest_tweet.id
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(f"New Tweet from @{USERNAME}: {latest_tweet.content}\nhttps://twitter.com/{USERNAME}/status/{latest_tweet.id}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    while True:
        await fetch_tweets()
        await asyncio.sleep(10)  # Runs every 10 seconds

client.run(TOKEN)
