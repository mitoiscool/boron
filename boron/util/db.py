import sqlite3
from flask import current_app

def read_db(query: str, args: tuple = tuple()) -> list:
    with sqlite3.connect(current_app.cfg['db_name']) as sqlite3_conn:
        sqlite3_conn.row_factory = sqlite3.Row
        return sqlite3_conn.cursor().execute(query, args).fetchall()