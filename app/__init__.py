from flask import Flask
from dotenv import load_dotenv


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)

    load_dotenv()

    with app.app_context():
        from .routes import configure_routes

        configure_routes(app)

    return app
