from flask import (
    Blueprint,
    redirect,
    Response,
)

root = Blueprint("root", __name__)


@root.get("/")
def index() -> Response:
    return redirect("https://github.com/mitoiscool/boron")
