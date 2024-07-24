from boron.util.db import query
import bcrypt
from boron.util.general import rnd_str
from flask import abort, request
from loguru import logger
from records import Record


def get_dev() -> Record:
    """
    Try to retrive session from current request and returns coresponding developer.
    Returns 401 if session is none or invalid.
    """
    s = request.cookies.get("session")
    if not s:
        return abort(401)
    res = query("SELECT * FROM developers WHERE session = :session", {"session": s})
    assert len(res) < 2
    if len(res) == 0:
        return abort(401)
    dev = res[0]
    logger.trace(f"{request.remote_addr} authorized as '{dev.email}', session = '{s}'")
    return dev


def register(email: str, password: str) -> str | None:
    if query("SELECT NULL FROM developers WHERE email = :email", {"email": email}):
        return "user already exists"
    logger.info(f"register developer {email}, password = '{password}'")
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    query(
        "INSERT INTO developers (email, password) VALUES (:email, :pass);",
        {"email": email, "pass": hashed_pass},
    )
    pass


def login(email: str, password: str):
    pswd = query(
        "SELECT password FROM developers WHERE email = :email;", {"email": email}
    )

    try:
        realPass = pswd[0].password
    except IndexError:
        realPass = None

    if realPass is None:  #  this may not work due to rows being returned
        return {"success": False, "message": "user does not exist"}

    if not bcrypt.checkpw(password.encode("utf-8"), realPass):  #  invalid password
        return {"success": False, "message": "invalid password"}

    # else, create session token and assign it to user in db
    session = rnd_str(15)

    query(
        "UPDATE developers SET session = :session WHERE email = :email",
        {"session": session, "email": email},
    )

    logger.info(f"'{email}' successfully logged in, session = '{session}'")

    return {
        "success": True,
        "session": session,
    }  # return session for further manipulation


def logout(session: str):
    query(
        "UPDATE developers SET session = NULL WHERE session = :session",
        {"session": session},
    )


# used only for creating dev accounts, not for production!
def create_user(email: str, password: str):
    # nameAlreadyUsed = query("SELECT COUNT(1) FROM developers WHERE email = ?;", (email,))

    # if int(nameAlreadyUsed[]) == 1:
    #    abort(Response("Username already exists", 409)) # username already used, handle?

    hashedPass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    query(
        "INSERT INTO developers (email, password) VALUES (:email, :pass);",
        {"email": email, "pass": hashedPass},
    )


def logged_in() -> bool:
    session = request.cookies.get("session")
    if not session:
        return False
    res = query(
        "SELECT * FROM developers WHERE session = :session", {"session": session}
    )
    if len(res) != 1:
        return False
    return True
