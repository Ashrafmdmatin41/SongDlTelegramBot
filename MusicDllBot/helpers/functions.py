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
from pytube import Search, YouTube
from pytube.exceptions import AgeRestrictedError

from MusicDllBot.helpers.keyboards import cancel_keyboard
from MusicDllBot.helpers.ikb import ikb

buttons_dict = {}


def search_song(song_name: str, limit: int = 1):
    songs = Search(song_name)
    return songs.results[0:limit]


async def cancel_in_msg(msg):
    if "/cancel" in msg.text:
        await msg.reply_text("**Cancelled search!**")
        return True
    elif msg.text.startswith("/"):
        await msg.reply_text("**Cancelled search!**")
        return True
    else:
        return False


async def progress_function(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    current = (filesize - bytes_remaining) / filesize
    percent = ("{0:.1f}").format(current * 100)
    progress = int(50 * current)
    status = "█" * progress + "-" * (50 - progress)

    # await msg.edit(text=f"Downloading - `{percent}%`")
    print(f"Downloading - `{percent}%`")


def send_progress(current, total, msg):
    now = current / total
    percent = ("{0:.1f}").format(now * 100)
    msg.edit(text=f"Uploading - `{percent}%`")


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def mp4_to_mp3(mp4_path: str):
    mp3_path = mp4_path.split(".")[0] + ".mp3"
    os.rename(mp4_path, mp3_path)
    return mp3_path


async def send_song_results(
    c,
    m,
    song_name: str,
    limit: int,
):
    query_list = search_song(song_name=song_name, limit=limit)

    for yt in query_list:
        try:
            thumbnail_url = yt.thumbnail_url
            caption = yt.title
            streams = yt.streams.filter(only_audio=True)
        except AgeRestrictedError as aer:
            print(aer)
            continue
        except Exception as e:
            print(e)
            continue
        for stream in streams:
            filesize_mb = ("{0:.1f}").format(stream.filesize_mb)
            x = stream.abr
            abr = x.split("k")[0]
            buttons_dict[f"🎙 {x} {filesize_mb}MB"] = f"stream={yt}={abr}"
        download_keyboard = ikb(buttons_dict)

        await c.send_photo(
            chat_id=m.chat.id,
            photo=thumbnail_url,
            caption=f"`{caption}`\n\n**Click below button to download**",
            reply_markup=download_keyboard,
        )


async def send_link_results(c, m, url: str):
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    caption = yt.title
    streams = yt.streams.filter(only_audio=True)
    for stream in streams:
        filesize_mb = ("{0:.1f}").format(stream.filesize_mb)
        x = stream.abr
        abr = x.split("k")[0]
        buttons_dict[f"🎙 {x} {filesize_mb}MB"] = f"stream={yt}={abr}"
    download_keyboard = ikb(buttons_dict)
    await c.send_photo(
        chat_id=m.chat.id,
        photo=thumbnail_url,
        caption=f"`{caption}`\n\n**Click below button to download**",
        reply_markup=download_keyboard,
    )


async def download_stream(c, cbq):
    download_output_path = os.path.join("downloads", str(cbq.message.chat.id))
    await cbq.message.edit(text="**🎙 Downloading...**")
    video_id = cbq.data.split("=")[-2].split(">")[0]
    abr = cbq.data.split("=")[-1]
    ytUrl = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(ytUrl)
    stream = yt.streams.filter(abr=f"{abr}kbps", only_audio=True)[0]
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
