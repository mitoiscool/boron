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
from boron.util.db import query
from boron.util.general import get_developer

application = Blueprint("application", __name__, url_prefix="/applications/")

@application.get("home")
def applications_home():
    dev = get_developer(request.cookies.get['session'])
    
    return render_template("panel/panel_home.html", dev = dev, apps=query("SELECT * FROM applications WHERE dev_id = ?", (dev.id,)))

# Create app (post)
@application.post("create")
def create_app():

    #if not logged_in(request):
        #return make_response(redirect(url_for(auth.login)))
    return ""

# Delete app (post)
@application.post("<appid>/delete")
def delete_app():

    #if not logged_in(request):
        #return make_response(redirect(url_for(""")))
    return ""

# App home page
@application.get("<appid>/view")
def get_app(appid):

    #if not logged_in(request):
        #return make_response(redirect(url_for(auth.login)))
    return ""

# App keys page
@application.get("<appid>/keys/")
def get_app_keys(appid):

    #if not logged_in(request):
        #return make_response(redirect(url_for(auth.login)))
    return ""

# App users page
@application.get("<appid>/users/")
def get_app_users(appid):

    #if not logged_in(request):
        #return make_response(redirect(url_for(auth.login)))
    return ""

#@application.context_processor
#def populate_ctx():
#    return {
        # get user info
        #request.cookies.get('session')
#    }