import os

from pyrogram import filters
from pyrogram import __version__ as PYRO_VERSION
from pyrogram.types import Message, CallbackQuery

from MusicDllBot import bot, BOT_USERNAME, VERSION, BOT_NAME
from MusicDllBot.helpers.functions import (
    create_dir,
    send_song_results,
    send_link_results,
    download_stream,
    cancel_in_msg
)
from MusicDllBot.helpers.keyboards import home_keyboard, help_keyboard, about_keyboard
from MusicDllBot.decorators.force_sub import force_sub


@bot.on_message(filters.command("start"))
@force_sub
async def start(c: bot, m: Message):
    global start_text
    start_text = f"""Hey! 🩷 {m.from_user.mention}, welcome to @{BOT_USERNAME}.

**I'm a youtube music downloader bot.**

Developed with 🩵
- @minkxx69"""
    await c.send_message(
        chat_id=m.chat.id,
        text=start_text,
        reply_to_message_id=m.id,
        reply_markup=home_keyboard,
    )


@bot.on_callback_query(filters.regex("home_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    await cbq.message.edit(text=start_text, reply_markup=home_keyboard)


@bot.on_callback_query(filters.regex("help_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    help_text = f"""**Help Menu - {BOT_USERNAME} 🤖**
    
/search -> open dialouge box to enter song name

/search __limit__ -> open dialouge box to enter song name and gives results

/search __song_name__ -> search the song

/search __song_name__ __limit__ -> search the song and gives results

**Or just send youtube link to download it.**"""

    await cbq.message.edit(text=help_text, reply_markup=help_keyboard)


@bot.on_callback_query(filters.regex("about_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    about_text = f"""**🤖 Bot Name :** `{BOT_NAME}`
**🛠 Bot Version :** `{VERSION}`
**⚒ Pyrogram Version :** `{PYRO_VERSION}`

**Developed by ~** 🩵 @minkxx69
"""
    await cbq.message.edit(text=about_text, reply_markup=about_keyboard)


@bot.on_callback_query(filters.regex("close_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    await cbq.message.delete()


@bot.on_message(filters.command("search"))
@force_sub
async def search_song(c: bot, m: Message):

    # create user directory
    path = os.path.join("downloads", str(m.chat.id))
    create_dir(path)

    # take user input for song name
    cmd = m.command
    limit = 1
    if len(cmd) > 1 and not cmd[-1].isdigit():
        song_name = " ".join(cmd[1:])
    elif len(cmd) > 2 and cmd[-1].isdigit():
        song_name = " ".join(cmd[1:-1])
        limit = int(cmd[-1])
    elif len(cmd) == 2 and cmd[1].isdigit():
        song = await c.ask(chat_id=m.chat.id, text="🎵 **Enter song name**\n/cancel - to cancel search")
        if await cancel_in_msg(song):
            return
        song_name = song.text
        limit = int(cmd[1])
    else:
        # asks user to enter song name
        song = await c.ask(chat_id=m.chat.id, text="🎵 **Enter song name**\n/cancel - to cancel search")
        if await cancel_in_msg(song):
            return
        song_name = song.text

    # search for song
    x = await c.send_message(chat_id=m.chat.id, text="🔎 __Searching...__")

    await send_song_results(c, m, song_name, limit)

    await x.delete()


@bot.on_message(filters.regex(pattern=r"https://youtu\.be/[a-zA-Z0-9_-]+(\?[a-zA-Z0-9_=-]+)?"))
@force_sub
async def yt_links_dl(c: bot, m: Message):
    path = os.path.join("downloads", str(m.chat.id))
    create_dir(path)
    url = m.text
    x = await c.send_message(
        chat_id=m.chat.id,
        text=f"🔎 __Searching...__",
        reply_to_message_id=m.id,
    )
    await send_link_results(c, m, url)
    await x.delete()


@bot.on_callback_query(filters.regex(pattern="^(stream=.)"))
async def dll(c: bot, cbq: CallbackQuery):
    path = os.path.join("downloads", str(cbq.message.chat.id))
    create_dir(path)
    await download_stream(c, cbq)


# @bot.on_callback_query(filters.regex(pattern="cancel_data"))
# async def delete_msg(c: bot, cbq: CallbackQuery):
#     path = os.path.join("downloads", str(cbq.message.chat.id))
#     await cbq.message.delete()
#     await c.send_message(chat_id=cbq.message.chat.id, text="**Download canceled!**")
#     for i in os.listdir(path):
#         os.remove(i)
