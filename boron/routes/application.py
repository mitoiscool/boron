from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    make_response
)
from boron.util.authenticator import logged_in
from boron.routes.auth import auth

application = Blueprint("application", __name__, url_prefix="/applications/")

@application.get("home")
def applications_home():

    if not logged_in(request):
        return make_response(redirect(url_for(auth.login))) # NOTE THIS DOES NOT WORK DO TO CIRCULAR IMPORTS
    

    return ""

# Create app page
@application.get("create")
def get_create_app():

    if not logged_in(request):
        return make_response(redirect(url_for(auth.login)))
    return ""

# Create app (post)
@application.post("create")
def create_app():

    if not logged_in(request):
        return make_response(redirect(url_for(auth.login)))
    return ""

# Delete app (post)
@application.post("/delete")
def delete_app():

    if not logged_in(request):
        return make_response(redirect(url_for(auth.login)))
    return ""

# App home page
@application.get("<appid>/")
def get_app(appid):

    if not logged_in(request):
        return make_response(redirect(url_for(auth.login)))
    return ""

# App keys page
@application.get("<appid>/keys/")
def get_app_keys(appid):

    if not logged_in(request):
        return make_response(redirect(url_for(auth.login)))
    return ""

# App users page
@application.get("<appid>/users/")
def get_app_users(appid):

    if not logged_in(request):
        return make_response(redirect(url_for(auth.login)))
    return ""