from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
)
from boron.util.general import gen_license

api = Blueprint("api", __name__, url_prefix="/api/")

@api.post("client/new")
def register_user():
    """Use license key, initialize expiration date and create use
    
    args:
    username
    password
    appid
    dyn_args (could be hwid, license key, depends what app has set up)
    """

@api.post("client/login")
def login_user():
    """Use license key, initialize expiration date and create use
    
    args:
    username
    password
    license_key
    appid

    """



