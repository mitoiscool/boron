from flask import current_app
from loguru import logger
from typing import Iterable, List
from records import Record


def query(query: str, args: dict = {}) -> List[Record]:
    """
    Execute query over database, cache all results and return.
    """
    return [row for row in query_it(query, args)]


def query_it(query: str, args: dict = {}) -> Iterable[Record]:
    """
    Execute query over database, return an iterator.
    """
    logger.trace(f"database: query = '{query}', args = {args}")
    return current_app.db.query(query, **args)
