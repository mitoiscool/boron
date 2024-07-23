from boron.util.db import query, record_exists
from boron.util.general import rnd_str
from datetime import datetime, timedelta
import bcrypt


def key_valid(license, appid):
    licenseKey = query("SELECT * FROM licensekeys WHERE name = :license AND app_id = :appid", {"license": license, "appid": appid})

    if not licenseKey:
        return {"success": False, "message": "License key does not exist."}
    
    if licenseKey[0].used == 1:
        return {"success": False, "message": "License key has already been used."}
    
    return True

def redeem_key(userid, license, appid):
    licenseKey = query("SELECT * FROM licensekeys WHERE name = :license AND app_id = :appid", {"license": license, "appid": appid})

    if not licenseKey:
        return {"success": False, "message": "License key does not exist."}
    
    if licenseKey[0].used == 1:
        return {"success": False, "message": "License key has already been used."}

    # then calculate expiration relative to key, set key to used
    # then add record to app_users to link the app to the user with expiration
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=licenseKey[0].length)

    # set key to used
    query("UPDATE licensekeys SET used = '1' WHERE name = :license AND app_id = :appid;", {"license": license, "appid": appid})

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

    if record_exists("SELECT id FROM users WHERE username = :username;", {"username": username}):
        return {"success": False, "message": "User already exists."}
    
    keyResp = key_valid(license, appid)
    if keyResp != True:
        return keyResp

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

    if not record_exists("SELECT id FROM users WHERE username = :username;", {"username": username}):
        return {"success": False, "message": "User does not exist."}
    
    # compare password

    realPass = query("SELECT password FROM users WHERE username = :username;", {"username": username})[0].password

    if not bcrypt.checkpw(password.encode("utf-8"), realPass):  #  invalid password
        return {"success": False, "message": "Your password is incorrect"}
    
    session = rnd_str(15)

    query(
        "UPDATE users SET session = :session WHERE username = :username;",
        {"session": session, "username": username},
    )

    return {
        "success": True,
        "session": session,
    }  # return session for further manipulation

def logout(session, appid):
    if not record_exists("SELECT id FROM users WHERE session = :sess;", {"sess": session}):
        return {"success": False, "message": "Session does not exist"}
    
    query("UPDATE users SET session = '' WHERE session = :sess;", {"sess": session})

    return {"success": True}

def set_data(username, appid):
    if not record_exists("SELECT id FROM users WHERE username = :us;", {"us": username}):
        return {"success": False, "message": "User does not exist"}
    


def get_userdata(username, appid):
    userIds = query("SELECT id FROM users WHERE username = :user", {"user": username})

    print(userIds)

    if not userIds:
        return {"success": False, "message": "Could not find user."}

    # chatgpt pls work
    resp = query("SELECT data FROM app_user WHERE app_id = :appid AND user_id = :userid", {"appid": appid, "userid": userIds[0].id})

    if not resp:
        return {"success": False, "message": "Could not find user data."}
    
    return resp[0].data

def set_userdata(username, appid, data):
    userIds = query("SELECT id FROM users WHERE username = :user", {"user": username})

    print(userIds)

    if not userIds:
        return {"success": False, "message": "Could not find user."}
    
    query("UPDATE app_user SET data = :userdata WHERE user_id = :uid AND app_id = :appid", {"userdata": data, "uid": userIds[0].id, "appid": appid})
    
    return {"success": True}