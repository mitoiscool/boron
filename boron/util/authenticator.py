from boron.util.db import query
import bcrypt
from boron.util.general import rnd_string
from flask import abort, Response


def login(email: str, password: str):
    realPass = query(
        "SELECT password FROM developers WHERE email = :email;", {"email": email}
    )[0].password

    if not realPass:  #  this may not work due to rows being returned
        return {"success": False, "message": "User does not exist."}

    if not bcrypt.checkpw(password.encode("utf-8"), realPass):  #  invalid password
        return {"success": False, "message": "Invalid password."}

    # else, create session token and assign it to user in db
    session = rnd_string(15)

    query(
        "UPDATE developers SET session = :session WHERE email = :email",
        {"session": session, "email": email},
    )
    return {
        "success": True,
        "session": session,
    }  # return session for further manipulation


def logout(session):
    query(
        "UPDATE developers SET session = 'logged out' WHERE session = :session",
        {"session": session},
    )


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


def logged_in(request) -> bool:
    session = request.cookies.get("session")
    if session is None:
        return False

    if (
        len(
            query(
                "SELECT email FROM developers WHERE session = :session",
                {"session": session},
            )
        )
        == 0
    ):
        return False  # check if session exists in db

    return True
