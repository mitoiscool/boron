import sqlite3
from flask import current_app
import records

def query(query: str, args: tuple = tuple()):
    database = records.Database(current_app.cfg['db_path'])
    return database.query(str, args)