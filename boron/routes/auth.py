from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    make_response
)
import sqlite3
from boron.routes.application import application

auth = Blueprint("auth", __name__, url_prefix="/auth/")

@auth.get("login")
def get_login():
    return render_template("/auth/login.html")

@auth.post("login")
def login():
    return make_response(redirect(url_for(application.applications_home)))

# Developer Register

@auth.get("register")
def get_register():
    return render_template("/auth/register.html")

@auth.post("register")
def register():
    """
    args:

    email
    pass
    cpass (confirm password serverside)

    """

    return make_response(redirect(url_for(application.applications_home)))