from db import query
from flask import abort

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

def get_application_users(dev, appid):
    if not appid:
        abort(422) # unprocessable request
    
    # query the app-users map to find all uids for this app, then return a list from the raw users table based on uids
        
    userIds = query("SELECT user_id FROM app_user WHERE app_id = ?", (appid,))

    users = query("") # use execute many, iterate through users
        
def create_application_user(dev, appid, user, password):

    """
    Insert into users table, and also add to the user/app map
    Probably should verify they do not already exist
    """

    return ""