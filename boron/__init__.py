from flask import Flask
from records import Database
import json
from loguru import logger
from sys import stdout

logger.remove(0)
logger.add(stdout, level="TRACE")

logger.debug("logger initialized")


def create_app():
    app = Flask(__name__)
    from boron.routes.auth import auth
    from boron.routes.application import application
    from boron.routes.api import api

    app.register_blueprint(auth)
    app.register_blueprint(application)
    app.register_blueprint(api)

    app.cfg = json.load(open("config.json"))
    app.db = Database(app.cfg["db_path"], isolation_level="AUTOCOMMIT").get_connection()

    return app
