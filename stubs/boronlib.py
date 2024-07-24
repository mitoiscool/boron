from flask import make_response, redirect, url_for
import requests

url_base = "https://www.boron.dev/api/"
app_id = 2

def get_user_data(req):
    session = req.cookies.get('session')

    if not session:
        return {"success": False, "message": "Session not valid. Is the user logged in?"}
    
    resp = requests.post(url_base + "/user/get", json={
        "appid": app_id,
        "session": session
    })

    return resp.text

def set_user_data(req, data):
    session = req.cookies.get('session')

    if not session:
        return {"success": False, "message": "Session not valid. Is the user logged in?"}
    
    resp = requests.post(url_base + "/user/set", json={
        "appid": app_id,
        "session": session,
        "data": data
    })

# form: username, password
def login(req, redirect_loc):

    username = req.form.get('username')
    password = req.form.get('password')

    resp = requests.post(url_base + "client/login", json={
        "user": username,
        "pass": password,
        "app_id": app_id
    }).json()

    if resp['success'] != 'true':
        return resp
    
    response = make_response(redirect(url_for(redirect_loc)))
    response.set_cookie("session", resp["session"], max_age=3600)

    return response

# form: username, password, licensekey
def register(request, redirect_loc):
    username = request.form.get('username')
    password = request.form.get('password')
    license = request.form.get('licensekey')

    resp = requests.post(url_base + "client/register", json={
        "user": username,
        "pass": password,
        "licensekey": license,
        "app_id": app_id
    }).json()

    if resp['success'] != 'true':
        return resp
    
    response = make_response(redirect(url_for(redirect_loc)))
    response.set_cookie("session", resp["session"], max_age=3600)

    return response

def logout(request, redirect_loc):
    resp = make_response(redirect(redirect_loc))
    session = request.cookies.get('session')

    if not session:
        return resp # already logged out?
    
    requests.post(url_base + "client/logout", json = {
        "session": session,
        "app_id": app_id
    })

    return resp

def is_logged_in(request):

    session = request.cookies.get('session')
    if not session:
        return False
    
    resp = requests.post(url_base + "client/loggedin", json = {
        "session": session,
        "app_id": app_id
    }).json()

    return bool(resp['loggedin'])

