from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
)
from boron.util.general import gen_license
from boron.util.db import query
from boron.util.appuser import create, login, logout, get_userdata, set_userdata
from datetime import datetime, timedelta
from boron.util.authenticator import create_user


api = Blueprint("api", __name__, url_prefix="/api/")


@api.post("client/register")
def register_user():
    """Use license key, initialize expiration date and create use

    args:
    username
    password
    app_id
    license
    """

    formUsername = request.form.get("user")
    formPassword = request.form.get("pass")

    formLicense = request.form.get("licensekey")
    formAppId = request.form.get("app_id")

    # get license key info

    resp = create(formUsername, formPassword, formLicense, formAppId)

    if not resp["success"]:
        return resp

    return login(formUsername, formPassword, formAppId)


@api.post("client/login")
def login_user():
    """Login, return session

    args:
    username
    password
    app_id

    """

    formUsername = request.form.get("user")
    formPassword = request.form.get("pass")

    formAppId = request.form.get("app_id")

    return login(formUsername, formPassword, formAppId)


@api.post("client/logout")
def logout_user():
    """Logout

    args:
    session
    app_id

    """

    formSess = request.form.get("session")

    formAppId = request.form.get("app_id")

    return logout(formSess, formAppId)


@api.post("client/loggedin")
def loggedin_user():
    """Loggedin

    args:
    session
    appid

    returns:
    bool true/false
    """

    formSess = request.form.get("session")

    return {
        "loggedin": bool(
            query("SELECT NULL FROM users WHERE session = :sess", {"sess": formSess})
        )
    }


@api.post("user/get")
def get_user():
    """Use appid and username to locate user

    args:

    appid
    username

    """
    appid = request.form.get("appid")
    user = query(
        "SELECT username FROM users WHERE session = :session",
        {"session": request.form.get("session")},
    )

    if not user:
        return {"success": False, "message": "Could not find session."}

    userData = get_userdata(user[0].username, appid)

    if not userData:
        return "none"
    return userData


@api.post("user/set")
def set_user():
    """Use appid and username to locate user

    args:

    appid
    session
    data

    """
    appid = request.form.get("appid")
    user = query(
        "SELECT username FROM users WHERE session = :session",
        {"session": request.form.get("session")},
    )

    if not user:
        return {"success": False, "message": "Could not find session."}

    return set_userdata(user[0].username, appid, request.form.get("data"))


@api.post("client/redeem")
def redeem_user():
    """Use license key, initialize expiration date and create use

    args:

    session
    appid
    licensekey

    """


@api.post("create_admin/<password>/")
def create_admin(password):
    if password != "caiuscaiuscaius":
        abort(404)

    create_user(request.form.get("user"), request.form.get("pass"))
    return "success"
