import os
from pytube import Search, YouTube
from pytube.exceptions import AgeRestrictedError

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def search_song(song_name: str, limit: int = 1):
    songs = Search(song_name)
    return songs.results[0:limit]


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


async def send_link_results(c, m, url: str):
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


async def download_stream(c, cbq):
    download_output_path = os.path.join("downloads", str(cbq.message.chat.id))
    await cbq.message.edit(text=f"**🎙 Downloading...**")
    video_id = cbq.data.split("=")[-1].split(">")[0]
    ytUrl = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(ytUrl)
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
