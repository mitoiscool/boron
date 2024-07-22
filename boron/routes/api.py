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
from boron.util.appuser import create
from datetime import datetime, timedelta


api = Blueprint("api", __name__, url_prefix="/api/")

@api.post("client/register")
def register_user():

    """Use license key, initialize expiration date and create use
    
    args:
    username
    password
    appid
    license
    """

    formUsername = formLicense = request.form.get('user')
    formPassword = formLicense = request.form.get('pass')

    formLicense = request.form.get('licensekey')
    formAppId = request.form.get('app_id')

    # get license key info

    return create(formUsername, formPassword, formLicense, formAppId)


@api.post("client/login")
def login_user():
    """Use license key, initialize expiration date and create use
    
    args:
    username
    password
    license_key
    appid

    """

@api.post("client/redeem")
def redeem_user():
    """Use license key, initialize expiration date and create use
    
    args:

    session
    appid
    licensekey

    """

