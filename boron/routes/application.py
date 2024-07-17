from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
)

application = Blueprint("application", __name__, url_prefix="/applications/")

@application.get("home")
def applications_home():
    return ""

# Create app page
@application.get("create")
def get_create_app():
    return ""

# Create app (post)
@application.post("create")
def create_app():
    return ""

# Delete app (post)
@application.post("/delete")
def delete_app():
    return ""

# App home page
@application.get("<appid>/")
def get_app(appid):
    return ""

# App keys page
@application.get("<appid>/keys/")
def get_app_keys(appid):
    return ""

# App users page
@application.get("<appid>/users/")
def get_app_users(appid):
    return ""