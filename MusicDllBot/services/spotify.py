import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Spotify:
    def __init__(self, spotify_client_id: str, spotify_client_secret: str):
        client_credentials_manager = SpotifyClientCredentials(
            spotify_client_id, spotify_client_secret
        )
        self.spotify = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )
        self.regex = r"^(https:\/\/open.spotify.com\/)(.*)$"

    def validUrl(self, url):
        if re.search(self.regex, url):
            return True
        else:
            return False

    def getTrack(self, url: str):
        if ("track" in url.split("/")) and (self.validUrl(url)):
            track = self.spotify.track(url)
            info = song_name = track["name"]
            cover_art_url = track["album"]["images"][2]["url"]
            for artist in track["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            return [info, cover_art_url, song_name]
        else:
            return "Not a valid spotify track"

    def getAlbum(self, url: str):
        if ("album" in url.split("/")) and (self.validUrl(url)):
            album = self.spotify.album(url)
            albumName = album["name"]
            cover_art_url = album["images"][2]["url"]
            results = []
            for item in album["tracks"]["items"]:
                info = item["name"]
                for artist in item["artists"]:
                    fetched = f' {artist["name"]}'
                    if "Various Artists" not in fetched:
                        info += fetched
                results.append(info)
            return [albumName, results, cover_art_url]
        else:
            return "Not a valid spotify track"

    def getPlaylist(self, url: str):
        if ("playlist" in url.split("/")) and (self.validUrl(url)):
            playlist = self.spotify.playlist(url)
            playlistName = playlist["name"]
            results = []
            for item in playlist["tracks"]["items"]:
                music_track = item["track"]
                info = music_track["name"]
                cover_art = music_track["album"]["images"][2]["url"]
                for artist in music_track["artists"]:
                    fetched = f' {artist["name"]}'
                    if "Various Artists" not in fetched:
                        info += fetched
                results.append([info, cover_art])
            return [playlistName, results]
        else:
            return "Not a valid spotify track"
