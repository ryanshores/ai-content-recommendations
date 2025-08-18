from flask import Flask

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    return app