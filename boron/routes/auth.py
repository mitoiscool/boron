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