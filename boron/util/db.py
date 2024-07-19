import sqlite3
from flask import current_app
import records


def query(query: str, args: dict = {}):
    print(f"boron.util.db.query: query = {query}, args = {args}")
    database = records.Database(current_app.cfg["db_path"])
    return database.query(query, **args)
