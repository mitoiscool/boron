import sqlite3
from flask import current_app

def query(query: str, args: tuple = tuple()) -> list:
    print(current_app.cfg['db_path'])
    with sqlite3.connect(current_app.cfg['db_path']) as sqlite3_conn:
        sqlite3_conn.row_factory = sqlite3.Row
        return sqlite3_conn.cursor().execute(query, args).fetchall()