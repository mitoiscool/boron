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

    if not logged_in(request):
        return make_response(redirect(url_for("auth.get_login")))
    
    dev = get_developer(request.cookies.get['session'])
    
    return render_template("panel/panel_home.html", dev = dev, apps=query("SELECT * FROM applications WHERE dev_id = ?", (dev.id,)))

# Create app (post)
@application.post("create")
def create_app():
    """
    Form args:
    appname
    """

    if not logged_in(request):
        return make_response(redirect(url_for("auth.get_login")))

    appName = request.form.get('appname')
    if not appName:
        abort(422) # unprocessable request

    dev = get_developer(request.cookies.get['session'])

    query("INSERT INTO applications (dev_id, name) VALUES (?, ?)", (dev.id, appName))

    return make_response(redirect(url_for("application.applications_home")))

# Delete app (post)
@application.post("<appid>/delete")
def delete_app(appid):


    if not logged_in(request):
        return make_response(redirect(url_for("auth.get_login")))

    if not appid:
        abort(422) # unprocessable request

    dev = get_developer(request.cookies.get['session'])

    # ensure it is the developer's app
    query("DELETE FROM applications WHERE dev_id = ? AND id = ?", (dev.id, appid))

    return make_response(redirect(url_for("application.applications_home")))

# App home page
@application.get("<appid>/view")
def get_app(appid):

    if not logged_in(request):
        return make_response(redirect(url_for("auth.get_login")))

    if not appid:
        abort(422) # unprocessable request

    dev = get_developer(request.cookies.get('session'))

    app = query("SELECT * FROM applications WHERE dev_id = ? AND id = ?", (dev.id, appid))

    if len(app) < 1:
        abort(404)

    return render_template("panel/app/app_home.html", dev=dev, app=app[0])

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