from boron.util.db import query
import bcrypt
from boron.util.general import rnd_string
from flask import abort, Response
from loguru import logger


def login(email: str, password: str):
    realPass = query(
        "SELECT password FROM developers WHERE email = :email;", {"email": email}
    )[0].password

    if not realPass:  #  this may not work due to rows being returned
        return {"success": False, "message": "user does not exist"}

    if not bcrypt.checkpw(password.encode("utf-8"), realPass):  #  invalid password
        return {"success": False, "message": "invalid password"}

    # else, create session token and assign it to user in db
    session = rnd_string(15)

    query(
        "UPDATE developers SET session = :session WHERE email = :email",
        {"session": session, "email": email},
    ).all()

    query("SELECT * FROM developers").all()

    logger.info(f"'{email}' successfully logged in, session = '{session}'")

    return {
        "success": True,
        "session": session,
    }  # return session for further manipulation


def logout(session):
    query(
        "UPDATE developers SET session = NULL WHERE session = :session",
        {"session": session},
    ).all()


# used only for creating dev accounts, not for production!
def create_user(email, password):
    # nameAlreadyUsed = query("SELECT COUNT(1) FROM developers WHERE email = ?;", (email,))

    # if int(nameAlreadyUsed[]) == 1:
    #    abort(Response("Username already exists", 409)) # username already used, handle?

    hashedPass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    query(
        "INSERT INTO developers (email, password) VALUES (:email, :pass);",
        {"email": email, "pass": hashedPass},
    )


def logged_in(session) -> bool:
    logger.trace(f"verifying session token '{session}'")

    res = query(
        "SELECT email FROM developers WHERE session = :session",
        {"session": session},
    )

    if len(res) == 0:
        return False  # check if session exists in db

    return True
