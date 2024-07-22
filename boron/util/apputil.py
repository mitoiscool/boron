from boron.util.db import query
from flask import abort
from boron.util.general import gen_license
from loguru import logger


def owns_app(dev, appid: int) -> bool:
    return (
        len(
            query(
                "SELECT NULL FROM applications WHERE id = :id AND dev_id = :dev_id",
                {"id": appid, "dev_id": dev.id},
            )
        )
        > 0
    )


def select_app(dev, appid):
    if not owns_app(dev, appid):
        return abort(403)
    res = query(
        "SELECT * FROM applications WHERE id = :id",
        {"id": appid},
    )
    assert len(res) == 1
    return res[0]


def delete_application(dev, appid: int):
    logger.info(f"deleting app{{id:{appid}}} as requested by {dev.email}")
    # we should probably also delete from license keys/users
    query("DELETE FROM app_user WHERE app_id = :app_id", {"app_id": appid})
    query("DELETE FROM licensekeys WHERE app_id = :app_id", {"app_id": appid})
    return query(
        "DELETE FROM applications WHERE dev_id = :dev_id AND id = :id",
        {"dev_id": dev.id, "id": appid},
    )


def get_user(user_id: int):
    return query("SELECT * FROM users WHERE id = :id", {"id": user_id})


def get_app_users(dev, appid) -> list:
    if not owns_app(dev, appid):
        return abort(403)
    # query the app-users map to find all uids for this app, then return a list from the raw users table based on uids
    users = query(
        "SELECT user_id as id, username, expiration FROM app_user JOIN users WHERE app_user.app_id = :app_id AND users.id = app_user.user_id",
        {"app_id": appid},
    )
    return users

def get_app_keys(dev, appid):
    if not owns_app(dev, appid):
        return abort(403)

    keys = query("SELECT * FROM licensekeys WHERE app_id = :app_id", {"app_id": appid})

    return keys


def gen_keys(dev, appid, count, length, prefix="BORON"):
    if not owns_app(dev, appid):
        return abort(403)

    key = [gen_license(prefix) for _ in range(count)]

    for k in key:
        query(
            "INSERT INTO licensekeys (name, length, app_id) VALUES (:name, :length, :app_id)",
            {"name": k, "length": length, "app_id": appid},
        )

    logger.info(f"{dev.email} generated {count} keys for app{{id:{appid}}}")

    return key

def get_securedata(dev, appid):
    if not owns_app(dev, appid):
        return abort(403)
    
    return query("SELECT * FROM data WHERE app_id = :appid;", {"appid": appid})

def edit_securedata(id, key, value, dev, appid):
    if not owns_app(dev, appid):
        return abort(403)
    
    query("UPDATE data SET keyname = :key, keyvalue = :value WHERE id = :id AND app_id = :appid;", {"key": key, "value": value, "id": id, "appid": appid})

def create_securedata(key, dev, appid):
    if not owns_app(dev, appid):
        return abort(403)
    
    query("INSERT INTO data (keyname, app_id) VALUES (:keyname, :appid);", {"keyname": key, "appid": appid})

def delete_securedata(id, dev, appid):
    if not owns_app(dev, appid):
        return abort(403)
    
    query("DELETE FROM data WHERE id = :id AND app_id = :appid", {"id": id, "appid": appid})