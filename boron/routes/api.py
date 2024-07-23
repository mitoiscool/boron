from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
)
from boron.util.general import gen_license
from boron.util.db import query, record_exists
from boron.util.appuser import create, login, logout
from datetime import datetime, timedelta


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

    formUsername = request.form.get('user')
    formPassword = request.form.get('pass')

    formLicense = request.form.get('licensekey')
    formAppId = request.form.get('app_id')

    # get license key info

    resp = create(formUsername, formPassword, formLicense, formAppId)

    if not resp['success']:
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

    formUsername = request.form.get('user')
    formPassword = request.form.get('pass')

    formAppId = request.form.get('app_id')

    return login(formUsername, formPassword, formAppId)

@api.post("client/logout")
def logout_user():
    """Logout
    
    args:
    session
    app_id

    """

    formSess = request.form.get('session')

    formAppId = request.form.get('app_id')

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

    formSess = request.form.get('session')
    formAppId = request.form.get('app_id')

    return {"loggedin": record_exists("SELECT id FROM users WHERE session = :sess AND appid = :appid", {"sess": formSess, "appid": formAppId})}

@api.post("client/redeem")
def redeem_user():
    """Use license key, initialize expiration date and create use
    
    args:

    session
    appid
    licensekey

    """

