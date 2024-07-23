from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    Response,
)
from loguru import logger
from boron.util.authenticator import get_dev
from boron.util.db import query
from boron.util.apputil import (
    select_app,
    delete_application,
    get_app_users,
    get_app_keys,
    gen_keys,
    get_securedata,
    edit_securedata,
    create_securedata,
    delete_securedata,
    delete_key,
    update_key,
)

application = Blueprint("application", __name__, url_prefix="/applications/")


@application.get("home")
def dev_home() -> Response:
    dev = get_dev()

    apps = query(
        "SELECT * FROM applications WHERE dev_id = :dev_id", {"dev_id": dev.id}
    )

    return render_template("panel/panel_home.html", dev=dev, apps=apps)


# Create app (post)
@application.post("create")
def create_app() -> Response:
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

    logger.info(f"{dev.email} created app '{appName}'")

    return make_response(redirect(url_for("application.dev_home")))


# Delete app (post)
@application.post("<int:appid>/delete")
def delete_app(appid: int) -> Response:
    dev = get_dev()

    delete_application(dev, appid)

    return make_response(redirect(url_for("application.dev_home")))


# App home page
@application.get("<int:appid>/view")
def get_app(appid: int) -> Response:
    dev = get_dev()

    app = select_app(dev, appid)

    return render_template(
        "panel/app/app_home.html",
        dev=dev,
        app=app,
        navbar="app",
        sidebar="home",
    )


# App users page
@application.get("<appid>/users/")
def get_app_user(appid) -> Response:
    dev = get_dev()

    app = select_app(dev, appid)

    return render_template(
        "panel/app/users.html",
        dev=dev,
        app=app,
        users=get_app_users(dev, appid),
        navbar="app",
        sidebar="user",
    )


# App keys page
@application.get("<int:appid>/keys/")
def get_app_key(appid) -> Response:
    dev = get_dev()

    keys = get_app_keys(dev, appid)

    return render_template(
        "panel/app/keys.html",
        dev=dev,
        keys=keys,
        app=select_app(dev, appid),
        navbar="app",
        sidebar="key",
    )


@application.post("<int:appid>/keys")
def post_app_key(appid) -> Response:
    dev = get_dev()
    form = request.form
    try:
        count, length, prefix = (
            int(form.get("count")),
            int(form.get("length")),
            "".join(form.get("prefix").split()),
        )
        if not prefix:
            prefix = "BORON"
        prefix = f"{prefix}XXXXX"[:5]
    except Exception:
        return abort(400)
    gen_keys(dev, appid, count, length, prefix)
    return redirect(url_for("application.get_app_key", appid=appid))


@application.post("<int:appid>/keys/<int:keyid>/update")
def update_app_key(appid, keyid) -> Response:
    dev = get_dev()
    form = request.form
    try:
        used = form.get("used")
        assert used in {"on", "off"}
        used = used == "on"
    except AssertionError:
        return abort(400)
    update_key(dev, appid, keyid, {"used": used})
    return redirect(url_for("application.get_app_key", appid=appid))


@application.post("<int:appid>/keys/<int:keyid>/delete")
def delete_app_key(appid, keyid) -> Response:
    dev = get_dev()
    delete_key(dev, appid, keyid)
    return redirect(url_for("application.get_app_key", appid=appid))


@application.get("<int:appid>/data")
def get_data(appid) -> Response:
    dev = get_dev()
    return render_template(
        "panel/app/data.html",
        dev=dev,
        app=select_app(dev, appid),
        data=get_securedata(dev, appid),
        navbar="app",
        sidebar="data",
    )


@application.post("<int:appid>/data/create")
def create_data(appid) -> Response:
    keyname = request.form.get("key")

    create_securedata(keyname, get_dev(), appid)

    return make_response(redirect(url_for("application.get_data", appid=appid)))


@application.post("<int:appid>/data/edit")
def edit_data(appid) -> Response:
    keyid = request.form.get("id")
    keyname = request.form.get("key")
    keyvalue = request.form.get("value")

    edit_securedata(keyid, keyname, keyvalue, get_dev(), appid)

    return make_response(redirect(url_for("application.get_data", appid=appid)))


@application.post("<int:appid>/data/delete")
def delete_data(appid) -> Response:
    keyid = request.form.get("id")

    delete_securedata(keyid, get_dev(), appid)

    return make_response(redirect(url_for("application.get_data", appid=appid)))


# @application.context_processor
# def populate_ctx():
#    return {
# get user info
# request.cookies.get('session')
#    }
