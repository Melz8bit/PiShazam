import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


def getToken():
    data = (
        "grant_type=client_credentials&client_id="
        + spotify_client_id
        + "&client_secret="
        + spotify_secret
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )
    response = response.json()
    if "error" in response:
        print("Error getting token")
        print(response)
        return

    access_token = response["access_token"]

    return access_token


def getImage(albumID):
    """
    Get the album art for the album with the given ID.
    """
    url = "https://api.spotify.com/v1/albums/" + albumID

    token = getToken()
    headers = {"Authorization": "Bearer " + token}

    response = requests.get(url, headers=headers)

    data = response.json()
    imageUrl = data["images"][0]["url"]

    f = open("./res/cover.jpg", "wb")
    f.write(requests.get(imageUrl).content)
    f.close()


def getAlbumTracks(albumID):
    tracks = {}

    url = "https://api.spotify.com/v1/albums/" + albumID + "/tracks"

    token = getToken()
    headers = {"Authorization": "Bearer " + token}

    response = requests.get(url, headers=headers)

    data = response.json()
    for song in data["items"]:
        tracks[song["track_number"]] = song["name"]

    with open("./res/track_list.txt", "w") as file:
        file.write(json.dumps(tracks))

    return tracks


def getIsrc(trackID):
    """
    Get the ISRC for the song with the given ID.
    """
    url = "https://api.spotify.com/v1/tracks/" + trackID

    token = getToken()
    headers = {"Authorization": "Bearer " + token}

    response = requests.get(url, headers=headers)

    data = response.json()
    isrc = data["external_ids"]["isrc"]
    return isrc
