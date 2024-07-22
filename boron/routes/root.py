from flask import (
    Blueprint,
    redirect,
    Response,
    url_for
)

root = Blueprint("root", __name__)


@root.get("/")
def index() -> Response:
    return redirect(url_for("auth.get_login"))
