from boron.util.db import query, record_exists
from datetime import datetime, timedelta
import bcrypt

def redeem_key(userid, license, appid):
    licenseKey = query("SELECT * FROM licensekeys WHERE name = :license AND app_id = :appid", {"license": license, "appid": appid})[0]

    if not licenseKey:
        return {"success": False, "message": "License key does not exist."}
    
    if licenseKey.used == 1:
        return {"success": False, "message": "License key has already been used."}

    # then calculate expiration relative to key, set key to used
    # then add record to app_users to link the app to the user with expiration
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=licenseKey.length)

    # set key to used
    query("UPDATE licensekeys SET used = '1' WHERE name = :license;", {"license": license})

    # apply user to application
    query(
        "INSERT INTO app_user (app_id, user_id, expiration) VALUES (:appid, :uid, :expir);",
        {"appid": appid, "uid": userid, "expir": expiration_date},
    )

    return {"success": True}

def create(username, password, license, appid):
    # first add user to users table

        # hash password
    
    # should check if user already exists

    if record_exists("SELECT id FROM users WHERE username = :username;", {"username": username, "appid": appid}):
        return {"success": False, "message": "User already exists."}

    hashedPass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    query(
        "INSERT INTO users (username, password) VALUES (:username, :pass);",
        {"username": username, "pass": hashedPass},
    )

    # get user id then redeem key

    user_id = query("SELECT id FROM users WHERE username = :uname;", {"uname": username})[0].id

    redeemResp = redeem_key(user_id, license, appid)
    
    if not redeemResp['success']:
        return redeemResp
    
    return {"success": True, "message": "User has been registered successfully."}

def login(username, password, appid):

    if not record_exists("SELECT id FROM users WHERE username = :username AND appid = :appid;", {"username": username, "appid": appid}):
        return {"success": False, "message": "User does not exist."}
    
    # compare password

    realPass = query("SELECT password FROM users WHERE username = :p")