import os
import requests

# Load environment variables
phone_number_id = os.getenv("PHONE_NUMBER_ID")
access_token = os.getenv("ACCESS_TOKEN")

url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}


def send_message(message, to):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": message},
    }

    try:
        print(f"Sending Message to {to}")
        response = requests.post(url, json=payload, headers=headers)
        print(f"Message sent: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
