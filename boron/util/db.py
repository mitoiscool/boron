import sqlite3
from flask import current_app
import records

database = records.Database(current_app.cfg['db_path'])

def query(query: str, args: tuple = tuple()):
    return database.query(str, args)