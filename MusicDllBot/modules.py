import os
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError

from pyrogram import filters
from pyrogram import __version__ as PYRO_VERSION
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from MusicDllBot import bot, BOT_USERNAME, VERSION, BOT_NAME
from MusicDllBot.helpers.functions import (
    search_song,
    progress_function,
    send_progress,
    create_dir,
    mp4_to_mp3,
)
from MusicDllBot.helpers.keyboards import home_keyboard, help_keyboard, about_keyboard


@bot.on_message(filters.command("start"))
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
        song = await c.ask(chat_id=m.chat.id, text="🎵 **Enter song name**")
        song_name = song.text
        limit = int(cmd[1])
    else:
        # asks user to enter song name
        song = await c.ask(chat_id=m.chat.id, text="🎵 **Enter song name**")
        song_name = song.text

    # search for song
    x = await c.send_message(chat_id=m.chat.id, text="🔎 __Searching...__", reply_to_message_id=m.id)
    query_list = search_song(song_name=song_name, limit=limit)

    # sends query to user chat
    for yt in query_list:
        try:
            thumbnail_url = yt.thumbnail_url
            caption = yt.title
            stream = yt.streams.filter(abr="160kbps")[0]
            filesize_mb = ("{0:.1f}").format(stream.filesize_mb)
        except AgeRestrictedError as aer:
            print(aer)
            continue
        except Exception as e:
            print(e)
            continue
        download_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"🎙 Download {filesize_mb}MB", callback_data=f"stream={yt}"
                    ),
                ],
                [
                    InlineKeyboardButton(text=f"❌ Close", callback_data=f"close_data"),
                ],
            ]
        )
        await c.send_photo(
            chat_id=m.chat.id,
            photo=thumbnail_url,
            caption=f"`{caption}`",
            reply_markup=download_keyboard,
        )
    await x.delete()


@bot.on_message(
    filters.regex(pattern=r"https://youtu\.be/[a-zA-Z0-9_-]+(\?[a-zA-Z0-9_=-]+)?")
)
async def yt_links_dl(c: bot, m: Message):
    path = os.path.join("downloads", str(m.chat.id))
    create_dir(path)
    url = m.text
    x = await c.send_message(chat_id=m.chat.id, text=f"🔎 __Searching...__", reply_to_message_id=m.id,)
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    caption = yt.title
    stream = yt.streams.filter(abr="160kbps")[0]
    filesize_mb = ("{0:.1f}").format(stream.filesize_mb)
    download_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"🎙 Download {filesize_mb}MB", callback_data=f"stream={yt}"
                ),
            ],
            [
                InlineKeyboardButton(text=f"❌ Close", callback_data=f"close_data"),
            ],
        ]
    )
    await c.send_photo(
        chat_id=m.chat.id,
        photo=thumbnail_url,
        caption=f"`{caption}`",
        reply_markup=download_keyboard,
    )
    await x.delete()


@bot.on_callback_query(filters.regex(pattern="^(stream=.)"))
async def download_stream(c: bot, cbq: CallbackQuery):
    path = os.path.join("downloads", str(cbq.message.chat.id))
    create_dir(path)
    download_output_path = os.path.join("downloads", str(cbq.message.chat.id))
    await cbq.message.edit(text=f"**🎙 Downloading...**")
    video_id = cbq.data.split("=")[-1].split(">")[0]
    ytUrl = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(
        ytUrl,
        # on_progress_callback=lambda stream, chunk, bytes_remaining:progress_function(stream, chunk, bytes_remaining)
    )
    stream = yt.streams.filter(abr="160kbps")[0]
    mp4_path = stream.download(output_path=download_output_path)
    await cbq.message.edit(text=f"Converting to mp3...")
    mp3_path = mp4_to_mp3(mp4_path)
    await c.send_audio(
        chat_id=cbq.message.chat.id,
        audio=mp3_path,
        caption=f"`{yt.title}`",
        duration=yt.length,
        title=f"{yt.title}",
        progress=lambda current, total: send_progress(current, total, cbq.message),
    )
    await cbq.message.delete()
    os.remove(mp3_path)


@bot.on_callback_query(filters.regex(pattern="close_data"))
async def delete_msg(c: bot, cbq: CallbackQuery):
    await cbq.message.delete()
