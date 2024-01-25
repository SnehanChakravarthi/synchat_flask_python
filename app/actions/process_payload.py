from app.actions.get_media import get_media
from app.actions.openAI_functions import (
    get_completion,
    get_text_from_audio,
    get_text_from_image,
)
from app.actions.send_message import send_message


def process_payload(payload):
    entries = payload.get("entry", [])

    for entry in entries:
        changes = entry.get("changes", [])

        for change in changes:
            message_data = change.get("value", {})
            messages = message_data.get("messages", [])

            for message in messages:
                from_number = message.get("from")
                message_type = message.get("type")

                if from_number and message_type:
                    try:
                        if message_type == "text":
                            process_text_message(message, from_number)
                        elif message_type == "audio":
                            process_audio_message(message, from_number)
                        elif message_type == "image":
                            process_image_message(message, from_number)
                    except Exception as error:
                        print(f"Error processing message: {error}")


def process_text_message(message, from_number):
    try:
        text_message = message.get("text")
        if text_message:
            message_content = text_message.get("body")
            print(f"Text message from {from_number}: {message_content}")
            chat_response = get_completion(message_content)
            if chat_response:
                send_message(chat_response.choices[0].message.content, from_number)
    except KeyError as e:
        print(f"KeyError: {e}")


def process_audio_message(message, from_number):
    try:
        audio_message = message.get("audio")
        if audio_message:
            message_content = {
                "mimeType": audio_message.get("mime_type"),
                "id": audio_message.get("id"),
            }
            print(f"Audio message from {from_number}: {message_content}")
            audio = get_media(
                message_content["id"], message_content["mimeType"], "audio"
            )

            transcript = get_text_from_audio(audio["filePath"])
            if transcript:
                transcript_text = transcript.text
                print("Transcript:", transcript_text)

                chat_response = get_completion(transcript_text)
                print("Chat Response:", chat_response)

            if chat_response:
                send_message(chat_response.choices[0].message.content, from_number)
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as error:
        print(f"Error processing audio message: {error}")


def process_image_message(message, from_number):
    try:
        image_message = message.get("image")
        if image_message:
            message_content = {
                "caption": image_message.get("caption"),
                "id": image_message.get("id"),
                "mimeType": image_message.get("mime_type"),
            }
            print(f"Image message from {from_number}: {message_content}")
            image = get_media(
                message_content["id"], message_content["mimeType"], "image"
            )
            if image and "filePath" in image:
                image_text = get_text_from_image(
                    image["filePath"], message_content["caption"]
                )
                if image_text:
                    send_message(image_text.choices[0].message.content, from_number)
            else:
                print("Error: Failed to download image or invalid image path.")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as error:
        print(f"Error processing image message: {error}")
