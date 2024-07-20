from flask import current_app
import records
from loguru import logger


def query(query: str, args: dict = {}):
    logger.trace(f"database: query = '{query}', args = {args}")
    return current_app.db.query(query, fetchall=True, **args)
