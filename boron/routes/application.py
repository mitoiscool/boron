from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    current_app,
)
from loguru import logger
from boron.util.authenticator import logged_in, session, get_dev
from boron.util.db import query
from boron.util.apputil import (
    owns_app,
    select_app,
    delete_application,
    get_application_users,
    get_application_keys,
)

application = Blueprint("application", __name__, url_prefix="/applications/")


@application.get("home")
def dev_home():
    print(request.cookies.get("session"))
    if not logged_in(session()):
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_dev()

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

    if not logged_in():
        return make_response(redirect(url_for("auth.get_login")))

    appName = request.form.get("appname")
    if not appName:
        abort(400)

    dev = get_dev()

    query(
        "INSERT INTO applications (dev_id, name) VALUES (:dev_id, :name)",
        {"dev_id": dev.id, "name": appName},
    )

    return make_response(redirect(url_for("application.dev_home")))


# Delete app (post)
@application.post("<int:appid>/delete")
def delete_app(appid: int):
    if not logged_in():
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_dev()

    delete_application(dev, appid)

    return make_response(redirect(url_for("application.dev_home")))


# App home page
@application.get("<int:appid>/view")
def get_app(appid: int):
    if not logged_in():
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_dev()

    if not owns_app(dev, appid):
        return abort(403)

    app = select_app(appid)

    return render_template("panel/app/app_home.html", dev=dev, app=app, page=1)


# App users page
@application.get("<appid>/users/")
def get_app_user(appid):
    if not logged_in():
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_dev()

    if not owns_app(dev, appid):
        return abort(403)

    app = select_app(appid)

    return render_template(
        "panel/app/users.html",
        dev=dev,
        users=get_application_users(dev, appid),
        page=2,
        app=app,
    )


# App keys page
@application.get("<appid>/keys/")
def get_app_key(appid):
    if not logged_in():
        return make_response(redirect(url_for("auth.get_login")))

    dev = get_dev()

    if not owns_app(dev, appid):
        return abort(403)

    keys = get_application_keys(dev, appid)

    return render_template(
        "panel/app/keys.html", dev=dev, keys=keys, page=3, app=select_app(appid)
    )


# @application.context_processor
# def populate_ctx():
#    return {
# get user info
# request.cookies.get('session')
#    }
