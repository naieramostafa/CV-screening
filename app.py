import os
from flask import Flask
from flask_cors import CORS

from config import Config
from api.routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    os.makedirs(Config.PUBLIC_FOLDER, exist_ok=True)

    app.register_blueprint(api)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT)
