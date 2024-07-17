from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
)

auth = Blueprint("auth", __name__, url_prefix="/auth/")

@auth.get("login")
def get_login():
    return render_template("/auth/login.html")

@auth.post("login")
def login():
    return ""

# Developer Register

@auth.get("register")
def get_register():
    return render_template("/auth/login.html")

@auth.post("register")
def register():
    return ""