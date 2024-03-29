import os
from pytube import Search


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
