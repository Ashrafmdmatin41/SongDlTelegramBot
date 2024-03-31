"""
Copyright (c) 2024 Minkxx

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import threading
import requests

from pyrogram import filters
from pyrogram import __version__ as PYRO_VERSION
from pyrogram.types import Message, CallbackQuery

from MusicDllBot import bot, BOT_USERNAME, VERSION, BOT_NAME, spotify, LOG_GROUP
from MusicDllBot.helpers.functions import (
    create_dir,
    send_song_results,
    send_link_results,
    download_stream,
    cancel_in_msg,
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
    
🎵 /search -> open dialouge box to enter song name

🎵 /search __limit__ -> open dialouge box to enter song name and gives results

🎵 /search __song_name__ -> search the song

🎵 /search __song_name__ __limit__ -> search the song and gives 

🎵 /lyrics -> open dialouge box to enter song name
🎵 /lyrics __song_name__ -> get lyrics of the song


**Or just send youtube link to download**
**Or send spotify link to download.**"""

    await cbq.message.edit(text=help_text, reply_markup=help_keyboard)


@bot.on_callback_query(filters.regex("about_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    about_text = f"""**🤖 Bot Name :** `{BOT_NAME}`
**🛠 Bot Version :** `{VERSION}`
**⚒ Pyrogram Version :** `{PYRO_VERSION}`

**⚙️ Supported Platforms**
- YouTube
- Spotify

**Developed by ~** 🩵 @minkxx69
"""
    await cbq.message.edit(text=about_text, reply_markup=about_keyboard)


@bot.on_callback_query(filters.regex("close_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    await cbq.message.delete()


@bot.on_message(filters.command("lyrics"))
@force_sub
async def send_lyrics(c: bot, m: Message):
    cmd = m.command
    if len(cmd) > 1:
        song_name: str = "+".join(cmd[1:])
    else:
        song = await c.ask(
            chat_id=m.chat.id,
            text="🎵 **Enter song name to get lyrics**\n/cancel - to cancel search",
        )
        if await cancel_in_msg(song):
            return
        song_name: str = (song.text).replace(" ", "+")

    x = await c.send_message(chat_id=m.chat.id, text="🔎 __Searching lyrics...__")

    try:
        print(song_name)
        url = f"https://apis.xditya.me/lyrics?song={song_name}"
        res = requests.get(url)
        data = res.json()
        lyrics = data["lyrics"]

        await c.send_message(
            chat_id=m.chat.id,
            text=f"`{lyrics}`",
        )

    except Exception as e:
        await c.send_message(
            chat_id=m.chat.id,
            text=f"**Can't find lyrics for** `{song_name}`",
        )
        await c.send_message(
            chat_id=LOG_GROUP,
            text=f"**Some error occured for chat** `{m.chat.id}`\n\n`{e}`",
        )

    await x.delete()


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
        song = await c.ask(
            chat_id=m.chat.id, text="🎵 **Enter song name**\n/cancel - to cancel search"
        )
        if await cancel_in_msg(song):
            return
        song_name = song.text
        limit = int(cmd[1])
    else:
        # asks user to enter song name
        song = await c.ask(
            chat_id=m.chat.id, text="🎵 **Enter song name**\n/cancel - to cancel search"
        )
        if await cancel_in_msg(song):
            return
        song_name = song.text

    # search for song
    x = await c.send_message(chat_id=m.chat.id, text="🔎 __Searching...__")

    send_search = threading.Thread(
        target=await send_song_results(c, m, song_name, limit)
    )
    send_search.start()

    await x.delete()


@bot.on_message(
    filters.regex(pattern=r"https://youtu\.be/[a-zA-Z0-9_-]+(\?[a-zA-Z0-9_=-]+)?")
)
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
    send_search_links = threading.Thread(target=await send_link_results(c, m, url))
    send_search_links.start()

    await x.delete()


@bot.on_callback_query(filters.regex(pattern="^(stream=.*=.*)$"))
async def dll(c: bot, cbq: CallbackQuery):
    path = os.path.join("downloads", str(cbq.message.chat.id))
    create_dir(path)
    await download_stream(c, cbq)
    # await test(c, cbq)


@bot.on_message(filters.regex(pattern=r"^(https:\/\/open.spotify.com\/)(.*)$"))
@force_sub
async def spotify_dl(c: bot, m: Message):
    url = m.text
    if "track" in url:
        data = spotify.getTrack(url)
        song_info = data[0]
        x = await c.send_message(
            chat_id=m.chat.id,
            text=f"🔎 __Searching...__",
            reply_to_message_id=m.id,
        )

        send_search = threading.Thread(
            target=await send_song_results(c, m, song_info, 1)
        )
        send_search.start()

        await x.delete()

    elif "album" in url:
        data = spotify.getAlbum(url)
        songs_info_list = data[1]
        x = await c.send_message(
            chat_id=m.chat.id,
            text=f"🔎 __Searching...__",
            reply_to_message_id=m.id,
        )
        length = len(songs_info_list)
        for song_info in songs_info_list:
            await x.edit(text=f"🔎 __Searching songs...__\n{length}. `{song_info}`")
            send_search = threading.Thread(
                target=await send_song_results(c, m, song_info, 1)
            )
            send_search.start()
            length -= 1

        await x.delete()

    elif "playlist" in url:
        data = spotify.getPlaylist(url)
        songs_list = data[1]
        x = await c.send_message(
            chat_id=m.chat.id,
            text=f"🔎 __Searching...__",
            reply_to_message_id=m.id,
        )
        length = len(songs_list)
        for i in songs_list:
            song_info = i[0]
            await x.edit(text=f"🔎 __Searching...__\n{length}. `{song_info}`")
            send_search = threading.Thread(
                target=await send_song_results(c, m, song_info, 1)
            )
            send_search.start()
            length -= 1

        await x.delete()
