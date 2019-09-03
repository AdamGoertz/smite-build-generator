import sqlite3
from typing import Dict, Any, Iterable
from data_objects.player import Player

class SmiteUserDatabase:
    DB_NAME = "smiteuserdb.db"

    def __init__(self, db_name: str):
        self.

    def __enter__(self):
        # Reopen connection on each call to ensure db is closed properly.
        # Database queries will be infrequent, so performance is not a major concern.
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
        return exc_type is not None


    def select(self, table: str, result_type: Any, *columns: Iterable[str], **selectors: Dict[str, Any]):
        with self as c:
            c.execute(f"""SELECT ({','.join(columns) if columns else '*'})
                          FROM {table} 
                          {('WHERE ' + ' AND '.join([f'{key} = ?' for key in selectors.keys()])) if selectors else ""};""", selectors.values())
            return tuple(result_type(res) for res in c.fetchall())


    def insert(self, table: str, **values: Dict[str, Any]):
        with self as c:
            c.execute(f"""INSERT INTO {table} ({','.join(values.keys())}) 
                          VALUES ({','.join(['?' for i in range(len(values))])});""", values.values())

    def update(self, table: str, selectors: Dict[str, Any], values: Dict[str, Any]):
        with self as c:
            c.execute(f"""UPDATE {table} 
                          SET {','.join([f'{key} = ?' for key in values.keys()])} 
                          WHERE {' AND '.join([f'{key} = ?' for key in selectors.keys()])};""", list(values.values()).extend(selectors.values()))

    def delete(self, table: str, **selectors: Dict[str, Any]):
        with self as c:
            c.execute(f"""DELETE FROM {table}
                          WHERE {' AND '.join([f'{key} = ?' for key in selectors.keys()])};""", selectors.values())


if __name__ == '__main__':
    sud = SmiteUserDatabase(":memory:")

    with sud as db:
        db.execute(f""""CREATE TABLE IF NOT EXISTS players (
                        id INTEGER PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL);""")

    sud.insert('players', name='Test', id=12345)
    print(sud.select('players', Player))