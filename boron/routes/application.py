from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
)
from boron.util.authenticator import logged_in, session
from boron.util.db import query
from boron.util.general import get_developer
from boron.util.apputil import (
    get_application,
    delete_application,
    get_application_users,
    get_application_keys,
)

application = Blueprint("application", __name__, url_prefix="/applications/")


@application.get("home")
def applications_home():
    if not logged_in(session()):
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_developer(request.cookies.get("session"))

    apps = query(
        "SELECT * FROM applications WHERE dev_id = :dev_id", {"dev_id": dev.id}
    )

    return render_template("panel/panel_home.html", dev=dev, apps=apps)


# Create app (post)
@application.post("create")
def create_app():
    """
    Form args:
    appname
    """

    if not logged_in(session()):
        return make_response(redirect(url_for("auth.get_login")))

    appName = request.form.get("appname")
    if not appName:
        abort(400)

    dev = get_developer(request.cookies.get("session"))

    query(
        "INSERT INTO applications (dev_id, name) VALUES (:dev_id, :name)",
        {"dev_id": dev.id, "name": appName},
    )

    return make_response(redirect(url_for("application.applications_home")))


# Delete app (post)
@application.route("<appid>/delete")
def delete_app(appid):
    if not logged_in(session()):
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_developer(request.cookies.get("session"))

    delete_application(dev, appid)

    return make_response(redirect(url_for("application.applications_home")))


# App home page
@application.get("<appid>/view")
def get_app(appid):
    if not logged_in(request):
        return make_response(redirect(url_for("auth.get_login")))

    if not appid:
        abort(422)  # unprocessable request

    dev = get_developer(request.cookies.get("session"))

    app = get_application(dev, appid)

    return render_template("panel/app/app_home.html", dev=dev, app=app, page=1)


# App users page
@application.get("<appid>/users/")
def get_app_users(appid):
    if not logged_in(request):
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_developer(request.cookies.get("session"))

    return render_template(
        "panel/app/app_home.html",
        dev=dev,
        users=get_application_users(dev, appid),
        page=2,
    )


# App keys page
@application.get("<appid>/keys/")
def get_app_keys(appid):
    if not logged_in(request):
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_developer(request.cookies.get("session"))

    keys = get_application_keys(dev, appid)

    return render_template("panel/app/app_home.html", dev=dev, keys=keys, page=3)


# @application.context_processor
# def populate_ctx():
#    return {
# get user info
# request.cookies.get('session')
#    }
