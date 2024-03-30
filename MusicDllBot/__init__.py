import os

from pyromod import Client

from MusicDllBot.services.spotify import Spotify

if os.path.exists("config.py"):
    from config import *
else:
    from sample_config import *

VERSION = "0.0.1"

bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

spotify = Spotify(
    spotify_client_id=SPOTIFY_CLIENT_ID, spotify_client_secret=SPOTIFY_CLIENT_SECRET
)

bot.start()
me = bot.get_me()
BOT_NAME = me.first_name + (me.last_name or "")
BOT_USERNAME = me.username

from MusicDllBot.modules import *
