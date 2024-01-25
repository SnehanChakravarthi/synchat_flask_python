from flask import request, Response
import os
import hashlib
import hmac
from functools import wraps
import json

from app.actions.process_payload import process_payload


# Load environment variables
verification_token = os.getenv("VERIFICATION_TOKEN")
app_secret = os.getenv("APP_SECRET")


def check_env_variables(f):
    """
    Decorator function to check if environment variables are set correctly.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not verification_token or not app_secret:
            return Response("Server configuration error", status=500)
        print("Environment variables are set correctly")
        return f(*args, **kwargs)

    return decorated_function


def validate_webhook_payload(f):
    """
    Decorator function to validate the webhook payload.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        Response: If the signature is not provided or invalid.

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        signature = request.headers.get("X-Hub-Signature-256")
        body = request.data

        if not signature:
            print("Signature not provided")
            return Response("Signature not provided", status=401)

        expected_signature = (
            "sha256=" + hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()
        )

        if signature != expected_signature:
            print("Invalid signature")
            return Response("Invalid signature", status=401)

        print("Webhook payload is valid")
        return f(*args, **kwargs)

    return decorated_function


def get_webhook():
    """
    Handles the verification of the webhook.

    This function is called when the webhook is being verified by the Whatsapp API.
    It checks the mode, token, and challenge parameters received in the request query string.
    If the mode is 'subscribe' and the token matches the verification token, it returns a
    successful response with the challenge value. Otherwise, it returns an error response.

    Returns:
        A Flask Response object with the appropriate status code and response body.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token and mode == "subscribe" and token == verification_token:
        print("WEBHOOK_VERIFIED")
        return Response(challenge, status=200)
    else:
        print("Invalid mode or token")
        return Response("Invalid mode or token.", status=403)


def post_webhook():
    payload = request.get_json()
    print(json.dumps(payload, indent=2))
    process_payload(payload)
    return Response(status=200)
