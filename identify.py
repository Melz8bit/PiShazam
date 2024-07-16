import json
import os
import requests
import spotifyapi as s

from dotenv import load_dotenv

load_dotenv()


def id_song():
    print("Identifying...")

    req_url = "https://api.audd.io/"
    api_key = os.getenv("AUDD_API_KEY")

    file_path = "test1.wav"

    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.audd.io/",
            data={"return": "apple_music,spotify", "api_token": api_key},
            files={"file": f},
        )

    r = response.json()

    if r["status"] == "success":
        title = r["result"]["title"]
        artist = r["result"]["artist"]
        album = r["result"]["spotify"]["album"]["name"]

        spotify_album_url = r["result"]["spotify"]["album"]["external_urls"]["spotify"]
        spotify_album_id = r["result"]["spotify"]["album"]["id"]
        spotify_artist_id = r["result"]["spotify"]["artists"][0]["external_urls"][
            "spotify"
        ]
        spotify_track_id = r["result"]["spotify"]["external_urls"]["spotify"]
        spotify_isrc = r["result"]["spotify"]["external_ids"]["isrc"]
        spotify_album_art = r["result"]["spotify"]["album"]["images"][0]["url"]

        track_list = s.getAlbumTracks(spotify_album_id)

        song_info = {
            "title": title,
            "artist": artist,
            "album": album,
            "spotify_album_id": spotify_album_url,
            "spotify_artist_id": spotify_artist_id,
            "spotify_track_id": spotify_track_id,
            "isrc": spotify_isrc,
            "track_list": track_list,
        }

        with open("./res/song_info.json", "w") as json_file:
            json.dump(song_info, json_file, indent=4, ensure_ascii=False)

        with open("./res/cover.jpg", "wb") as cover_art:
            cover_art.write(requests.get(spotify_album_art).content)

    else:
        print("Error: ", r["status"]["msg"])
