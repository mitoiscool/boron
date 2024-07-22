from flask import request, make_response, redirect, url_for
import requests

url_base = "https://boron.dev/api/client/"
app_id = 2

# form: username, password
def login(request, redirect_loc):

    username = request.form.get('username')
    password = request.form.get('password')

    resp = requests.post(url_base + "login", json={
        "username": username,
        "password": password,
        "app_id": app_id
    })

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

    resp = requests.post(url_base + "register", json={
        "username": username,
        "password": password,
        "licensekey": license,
        "app_id": app_id
    })

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
    
    requests.post(url_base + "logout", json = {
        "session": session,
        "app_id": app_id
    })

    return resp

def is_logged_in(request):

    session = request.cookies.get('session')
    if not session:
        return False
    
    resp = requests.post(url_base + "logout", json = {
        "session": session,
        "app_id": app_id
    })

    return bool(resp['loggedin'])

