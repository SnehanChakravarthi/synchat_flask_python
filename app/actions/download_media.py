import os
import base64
import requests

# Load environment variables
access_token = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {access_token}",
}


def download_media(download_url, mime_type, media):
    file_extension = mime_type.split("/")[1].split(";")[0]
    media_directory = os.path.join(os.path.dirname(__file__), "media")

    if not os.path.exists(media_directory):
        os.makedirs(media_directory)

    try:
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()

        if media == "image":
            # Convert binary data to base64
            base64_data = base64.b64encode(response.content).decode("utf-8")

            # Decode base64 data back into binary
            binary_data = base64.b64decode(base64_data)

            # Write binary data to image file
            file_path = os.path.join(media_directory, f"imageFile.{file_extension}")
            with open(file_path, "wb") as file:
                file.write(binary_data)

            return {"filePath": file_path}

        elif media == "audio":
            # Save binary data to file
            file_path = os.path.join(media_directory, f"mediaFile.{file_extension}")
            with open(file_path, "wb") as file:
                file.write(response.content)
            return {"filePath": file_path}

        else:
            raise ValueError(f"Unsupported media type: {media}")

    except requests.RequestException as error:
        print(f"Error downloading media: {error}")
        raise
