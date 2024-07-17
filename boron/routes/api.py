from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
)

api = Blueprint("api", __name__, url_prefix="/api/")