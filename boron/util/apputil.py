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


def ensure_owns_app(dev, appid: int):
    if not owns_app(dev, appid):
        return abort(403)


def select_app(dev, appid):
    ensure_owns_app(dev, appid)
    res = query(
        "SELECT * FROM applications WHERE id = :id",
        {"id": appid},
    )
    assert len(res) == 1
    return res[0]


def delete_application(dev, appid: int):
    ensure_owns_app(dev, appid)

    logger.info(f"deleting app{{id:{appid}}} as requested by {dev.email}")

    query("DELETE FROM app_user WHERE app_id = :app_id", {"app_id": appid})
    query("DELETE FROM licensekeys WHERE app_id = :app_id", {"app_id": appid})

    return query(
        "DELETE FROM applications WHERE dev_id = :dev_id AND id = :id",
        {"dev_id": dev.id, "id": appid},
    )


def get_user(id: int):
    return query("SELECT * FROM users WHERE id = :id", {"id": id})


def get_app_stat(dev, appid: int) -> dict:
    ensure_owns_app(dev, appid)

    res = {
        "user": count_user(dev, appid),
        "key": count_key(dev, appid),
        "data": count_securedata(dev, appid),
    }
    return res


def count_user(dev, appid: int) -> int:
    ensure_owns_app(dev, appid)

    users = query(
        "SELECT NULL FROM app_user JOIN users WHERE app_user.app_id = :app_id AND users.id = app_user.user_id",
        {"app_id": appid},
    )
    return len(users)


def get_app_users(dev, appid: int) -> list:
    ensure_owns_app(dev, appid)
    # query the app-users map to find all uids for this app, then return a list from the raw users table based on uids
    users = query(
        "SELECT user_id as id, username, expiration FROM app_user JOIN users WHERE app_user.app_id = :app_id AND users.id = app_user.user_id",
        {"app_id": appid},
    )
    return users


def count_key(dev, appid: int) -> int:
    ensure_owns_app(dev, appid)

    key = query(
        "SELECT NULL FROM licensekeys WHERE app_id = :app_id", {"app_id": appid}
    )
    return len(key)


def get_app_keys(dev, appid: int):
    ensure_owns_app(dev, appid)

    keys = query("SELECT * FROM licensekeys WHERE app_id = :app_id", {"app_id": appid})
    return keys


def gen_keys(dev, appid, count, length, prefix="BORON"):
    ensure_owns_app(dev, appid)

    key = [gen_license(prefix) for _ in range(count)]

    for k in key:
        query(
            "INSERT INTO licensekeys (name, length, app_id) VALUES (:name, :length, :app_id)",
            {"name": k, "length": length, "app_id": appid},
        )

    logger.info(f"{dev.email} generated {count} keys for app{{id:{appid}}}")
    return key


def count_securedata(dev, appid: int) -> int:
    ensure_owns_app(dev, appid)

    res = query(
        "SELECT NULL FROM secured_data WHERE app_id = :appid;", {"appid": appid}
    )
    return len(res)


def get_securedata(dev, appid):
    ensure_owns_app(dev, appid)

    return query("SELECT * FROM secured_data WHERE app_id = :appid;", {"appid": appid})


def edit_securedata(id, key, value, dev, appid):
    ensure_owns_app(dev, appid)

    query(
        "UPDATE secured_data SET key = :key, value = :value WHERE id = :id AND app_id = :appid;",
        {"key": key, "value": value, "id": id, "appid": appid},
    )


def create_securedata(key, dev, appid):
    ensure_owns_app(dev, appid)

    exist = query(
        "SELECT NULL FROM secured_data WHERE key = :key AND app_id = :app_id",
        {"key": key, "app_id": appid},
    )

    if exist:
        return abort(400)

    query(
        "INSERT INTO secured_data (key, app_id) VALUES (:key, :appid);",
        {"key": key, "appid": appid},
    )


def delete_securedata(id, dev, appid):
    ensure_owns_app(dev, appid)

    query(
        "DELETE FROM secured_data WHERE id = :id AND app_id = :appid",
        {"id": id, "appid": appid},
    )
