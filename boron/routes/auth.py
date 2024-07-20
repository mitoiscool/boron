from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    make_response,
)
from loguru import logger
from boron.routes.application import application
from boron.util.authenticator import login as lgn
from boron.util.authenticator import logout as lgo

auth = Blueprint("auth", __name__, url_prefix="/auth/")


@auth.get("login")
def get_login():
    return render_template("/auth/login.html")


@auth.post("login")
def login():
    """
    email
    pass

    make error field to display in login form
    """

    e, p = request.form.get("email"), request.form.get("pass")
    logger.trace(f"trying to login with email = '{e}', password = '{p}'")
    resp = lgn(e, p)

    if not resp["success"]:  # there was an error
        return render_template("/auth/login.html", error=resp["message"])

    response = make_response(redirect(url_for("application.applications_home")))
    response.set_cookie("session", resp["session"])

    return response


@auth.post("logout")
def logout():
    sessionToken = request.cookies["session"]
    if sessionToken is not None:
        # invalidate session in the db
        lgo(sessionToken)

    return make_response(redirect(url_for("auth.login")))
