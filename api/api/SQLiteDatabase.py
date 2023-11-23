from typing import List
from SQLDatabase import SQLDatabase
import sqlite3



SQLITE_TIMEOUT_SECONDS = 10


# Taken from https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLLiteDatabase(SQLDatabase):
    def __init__(self, path: str):
        self._conn = sqlite3.connect(path, timeout=SQLITE_TIMEOUT_SECONDS)
        self._conn.row_factory = dict_factory

    def query(self, query: str) -> List[dict]:
        cur = self._conn.cursor()
        result = cur.execute(query)
        return result.fetchall()
