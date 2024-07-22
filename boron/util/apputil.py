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
    return query(
        "DELETE FROM applications WHERE dev_id = :dev_id AND id = :id",
        {"dev_id": dev.id, "id": appid},
    )


def get_user(user_id: int):
    return query("SELECT * FROM users WHERE id = :id", {"id": user_id})


def get_application_users(dev, appid) -> list:
    if not owns_app(dev, appid):
        return abort(403)

    # query the app-users map to find all uids for this app, then return a list from the raw users table based on uids

    userIds = query(
        "SELECT user_id FROM app_user WHERE app_id = :app_id", {"app_id": appid}
    )

    return [get_user(i, appid) for i in userIds]


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


def create_application_user(dev, appid, user, password):
    """
    Insert into users table, and also add to the user/app map
    Probably should verify they do not already exist
    """

    return ""
