from .webhook_handler import (
    get_webhook,
    post_webhook,
    check_env_variables,
    validate_webhook_payload,
)


def configure_routes(app):
    """
    Configures the routes for the Flask application.

    Args:
        app (Flask): The Flask application object.

    Returns:
        None
    """
    app.add_url_rule(
        "/api/webhook", view_func=check_env_variables(get_webhook), methods=["GET"]
    )

    app.add_url_rule(
        "/api/webhook",
        view_func=check_env_variables(validate_webhook_payload(post_webhook)),
        methods=["POST"],
    )

    app.add_url_rule(
        "/api",
        view_func=lambda: "Hello, World!",
    )
