from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
)

main = Blueprint("main", __name__, url_prefix="/")

# Developer Login

@main.get("/auth/login")
def get_login():
    return render_template("/auth/login.html")

@main.post("/auth/login")
def login():
    return ""

# Developer Register

@main.get("/auth/register")
def get_register():
    return render_template("/auth/login.html")

@main.post("/auth/register")
def register():
    return ""

# Applications Panel

# Home
@main.get("/applications/home")
def applications_home():
    return ""

# Create app page
@main.get("/applications/create")
def get_create_app():
    return ""

# Create app (post)
@main.post("/applications/create")
def create_app():
    return ""

# Delete app (post)
@main.post("/applications/delete")
def delete_app():
    return ""


# Specific app panel functionality


# App home page
@main.get("/applications/<appid>/")
def get_app(appid):
    return ""

# App keys page
@main.get("/applications/<appid>/keys/")
def get_app_keys(appid):
    return ""

# App users page
@main.get("/applications/<appid>/users/")
def get_app_users(appid):
    return ""