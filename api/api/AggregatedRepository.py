from SQLDatabase import SQLDatabase
from typing import List

QUERY = "select * from aggregated"


class AggregatedRepository:
    def __init__(self, db: SQLDatabase):
        self._db = db

    def get_all(self) -> List[dict]:
        return self._db.query(QUERY)
