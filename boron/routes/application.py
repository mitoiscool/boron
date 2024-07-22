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
from boron.util.authenticator import get_dev
from boron.util.db import query
from boron.util.apputil import (
    select_app,
    delete_application,
    get_application_users,
    get_app_keys,
    gen_keys,
)

application = Blueprint("application", __name__, url_prefix="/applications/")


@application.get("home")
def dev_home():
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
    dev = get_dev()

    appName = request.form.get("appname")
    if not appName:
        abort(400)

    query(
        "INSERT INTO applications (dev_id, name) VALUES (:dev_id, :name)",
        {"dev_id": dev.id, "name": appName},
    )

    logger.info(f"{dev.email} created app{{name:'{appName}'}}")

    return make_response(redirect(url_for("application.dev_home")))


# Delete app (post)
@application.post("<int:appid>/delete")
def delete_app(appid: int):
    dev = get_dev()

    delete_application(dev, appid)

    return make_response(redirect(url_for("application.dev_home")))


# App home page
@application.get("<int:appid>/view")
def get_app(appid: int):
    dev = get_dev()

    app = select_app(dev, appid)

    return render_template("panel/app/app_home.html", dev=dev, app=app, page=1)


# App users page
@application.get("<appid>/users/")
def get_app_user(appid):
    dev = get_dev()

    app = select_app(dev, appid)

    return render_template(
        "panel/app/users.html",
        dev=dev,
        app=app,
        users=get_application_users(dev, appid),
        sidebar="user",
    )


# App keys page
@application.get("<int:appid>/keys/")
def get_app_key(appid):
    dev = get_dev()

    keys = get_app_keys(dev, appid)

    return render_template(
        "panel/app/keys.html", dev=dev, keys=keys, page=3, app=select_app(dev, appid)
    )


@application.post("<int:appid>/keys")
def post_app_key(appid):
    dev = get_dev()
    form = request.form
    try:
        count, length, prefix = (
            int(form.get("count")),
            int(form.get("length")),
            form.get("prefix"),
        )
        if not prefix:
            prefix = "BORON"
        assert len(prefix) == 5
    except Exception:
        return abort(400)
    gen_keys(dev, appid, count, length, prefix)
    return redirect(url_for("application.get_app_key", appid=appid))


# @application.context_processor
# def populate_ctx():
#    return {
# get user info
# request.cookies.get('session')
#    }
