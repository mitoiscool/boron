from boron.util.db import query
from flask import abort
from boron.util.general import gen_license

def owns_app(dev, appid):
    return len(query("SELECT name FROM applications WHERE app_id = ? AND dev_id = ?", (appid, dev.id))) > 0
def get_application(dev, appid):

    if not appid:
        abort(422) # unprocessable request
    
    try:
        return query("SELECT * FROM applications WHERE dev_id = ? AND id = ?", (dev.id, appid))[0]
    except:
        abort(404)
def delete_application(dev, appid):
    if not appid:
        abort(422) # unprocessable request
    
    try:
        query("DELETE FROM applications WHERE dev_id = ? AND id = ?", (dev.id, appid))
    except:
        abort(404)
def get_application_user(userIdRecord, appId):
    try:
        if userIdRecord.app_id != appId:
            abort(403) // forbidden
        return query("SELECT * FROM users WHERE id = ", (userIdRecord.user_id,))
    except:
        abort(404)
def get_application_users(dev, appid):
    if not appid:
        abort(422) # unprocessable request

    if not owns_app(dev, appid):
        abort(403)

    # query the app-users map to find all uids for this app, then return a list from the raw users table based on uids
    
    userIds = query("SELECT * FROM app_user WHERE app_id = ?", (appid,))

    users = []

    for userId in userIds:
        users.append(
            get_application_user(userId, appid)
        )
def get_application_keys(dev, appid):
    if not owns_app(dev, appid):
        abort(403)
    
    keys = query("SELECT * FROM licensekeys WHERE app_id = ?", (appid,))

    return keys
def generate_app_keys(dev, appid, count, length):
    if not owns_app(dev, appid):
        abort(403)
    keys = []

    for i in range(count):
        key = gen_license()
        keys.append(key)
        query("INSERT INTO licensekeys (name, length, app_id) VALUES (?, ?, ?)", (key, length, appid))
    
    return keys
def create_application_user(dev, appid, user, password):
    """
    Insert into users table, and also add to the user/app map
    Probably should verify they do not already exist
    """

    return ""