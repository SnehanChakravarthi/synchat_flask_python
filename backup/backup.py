from flask import Flask, request, Response
import os
import hashlib
import hmac
from functools import wraps
from dotenv import load_dotenv
import json

app = Flask(__name__)

load_dotenv()

# Load environment variables
verification_token = os.getenv("VERIFICATION_TOKEN")
app_secret = os.getenv("APP_SECRET")


def check_env_variables(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not verification_token or not app_secret:
            return Response("Server configuration error", status=500)
        print("Environment variables are set correctly")
        return f(*args, **kwargs)

    return decorated_function


def validate_webhook_payload(f):
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


@app.route("/api/webhook", methods=["GET"])
@check_env_variables
def get_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token and mode == "subscribe" and token == verification_token:
        print("WEBHOOK_VERIFIED")
        return Response(challenge, status=200)
    else:
        print("Invalid mode or token")
        return Response("Invalid mode or token.", status=403)


@app.route("/api/webhook", methods=["POST"])
@check_env_variables
@validate_webhook_payload
def post_webhook():
    payload = request.get_json()
    print(json.dumps(payload, indent=2))
    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
