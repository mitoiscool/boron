from flask import Flask
from records import Database
import tomllib
from loguru import logger
from sys import stdout


def create_app():
    app = Flask(__name__)
    from boron.routes.auth import auth
    from boron.routes.application import application
    from boron.routes.api import api
    from boron.routes.root import root
    from boron.routes import error

    app.register_blueprint(auth)
    app.register_blueprint(application)
    app.register_blueprint(api)
    app.register_blueprint(root)
    app.register_error_handler(401, error.http_401)
    app.register_error_handler(403, error.http_403)
    app.register_error_handler(404, error.http_404)

    app.cfg = tomllib.load(open("config.toml", "rb"))
    logger.remove(0)
    logger.add(stdout, level=app.cfg["log-level"])
    logger.debug("logger initialized")
    app.db = Database(app.cfg["db-url"], isolation_level="AUTOCOMMIT").get_connection()

    return app
