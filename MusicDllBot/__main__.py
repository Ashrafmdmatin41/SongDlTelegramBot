import asyncio
import os
from pyrogram import idle
from MusicDllBot import bot, LOG_GROUP
from MusicDllBot.helpers.functions import create_dir

loop = asyncio.get_event_loop()


async def start_bot():
    print("Sending online status!")
    await bot.send_message(LOG_GROUP, "Bot Online!")
    print("Sent!")
    await idle()


if __name__ == "__main__":
    create_dir(os.path.join("downloads"))
    loop.run_until_complete(start_bot())
