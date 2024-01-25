import os
import requests

from app.actions.download_media import download_media

access_token = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {access_token}",
}


def get_media(id, mime_type, media):
    url = f"https://graph.facebook.com/v19.0/{id}/"

    try:
        response = requests.get(url, headers=headers)
        url = response.json()["url"]
        if url:
            return download_media(url, mime_type, media)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
