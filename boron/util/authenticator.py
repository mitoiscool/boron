from boron.util.db import query
import bcrypt
from boron.util.general import rnd_string
from flask import abort, Response

def login(email, password):

    realPass = query("SELECT password FROM developers WHERE username = ?;", (email))

    if not bcrypt.checkpw(password.encode('utf-8'), realPass): #  invalid password
        return {"success": False, "message": "Invalid Password"}
    
    # else, create session token and assign it to user in db
    session = rnd_string(15)

    query("UPDATE developers SET session = ? WHERE email = ?", (session, email))
    return {"success": True, "session": session}  # return session for further manipulation



    
    
    

# used only for creating dev accounts, not for production!
def create_user(email, password):
    #nameAlreadyUsed = query("SELECT COUNT(1) FROM developers WHERE email = ?;", (email,))

    #if int(nameAlreadyUsed[]) == 1:
    #    abort(Response("Username already exists", 409)) # username already used, handle?
    
    hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query("INSERT INTO developers (email, password) VALUES (?, ?);", (email, hashedPass))
