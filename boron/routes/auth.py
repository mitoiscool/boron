from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
)
from loguru import logger
from boron.util.authenticator import login as lgn, logout as lgo, get_dev


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
    logger.trace(f"{request.remote_addr} trying to login {e} with password = '{p}'")
    resp = lgn(e, p)

    if not resp["success"]:  # there was an error
        return render_template("/auth/login.html", error=resp["message"])

    response = make_response(redirect(url_for("application.dev_home")))
    response.set_cookie("session", resp["session"], max_age=3600)

    return response


@auth.route("logout")
def logout():
    dev = get_dev()
    logger.info(f"{dev.email} logged out session {dev.session}")
    lgo(dev.session)
    return make_response(redirect("/"))
