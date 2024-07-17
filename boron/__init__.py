from flask import Flask


def create_app():
    app = Flask(__name__)
    from boron.routes.auth import auth
    from boron.routes.application import application
    from boron.routes.api import api

    app.register_blueprint(auth)
    app.register_blueprint(application)
    app.register_blueprint(api)

    return app