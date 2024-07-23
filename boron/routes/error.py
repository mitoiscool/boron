from flask import render_template, url_for


def http_400(_):
    return render_template("httperr.html", code=400, msg="Bad Request"), 400


def http_401(_):
    return render_template(
        "httperr.html", code=401, msg="Unauthorized", url=url_for("auth.get_login")
    ), 401


def http_403(_):
    return render_template("httperr.html", code=403, msg="Forbidden"), 403


def http_404(_):
    return render_template("httperr.html", code=404, msg="Not Found"), 404
