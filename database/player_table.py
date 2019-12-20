from database.connection import SmiteDBConnection
from data_objects.player import Player
from typing import Optional, Type

class PlayerTable(SmiteDBConnection):
    TABLE = "players"

    def __init__(self, player_factory: Type[Player]):
        super().__init__()
        self.player_factory = player_factory
        self.cur = self.conn.cursor()

        with self.conn as c:
            c.execute(f"""CREATE TABLE IF NOT EXISTS {PlayerTable.TABLE} (
                      name TEXT NOT NULL,
                      id INTEGER PRIMARY KEY NOT NULL
                      );""")

    def add_player(self, player: Player) -> None:
        with self.conn:
            self.cur.execute(f"""INSERT OR REPLACE INTO {PlayerTable.TABLE} (name, id) VALUES (?, ?);""", (player.name, player.id))

    def remove_player(self, player: Player) -> None:
        with self.conn:
            self.cur.execute(f"""DELETE FROM {PlayerTable.TABLE} WHERE name = ? AND id = ?;""", (player.name, player.id))

    def get_player_by_name(self, name: str) -> Optional[Player]:
        # Currently returns only one Player object, even though there may potentially be multiple players with the same name in the database
        with self.conn:
            self.cur.execute(f"""SELECT * FROM {PlayerTable.TABLE} WHERE name = ?;""", (name,))
            res = self.cur.fetchone()
            return self.player_factory(*res) if res else None

    def get_player_by_id(self, id: int) -> Optional[Player]:
        with self.conn:
            self.cur.execute(f"""SELECT * FROM {PlayerTable.TABLE} WHERE id = ?;""", (id,))
            res = self.cur.fetchone()
            return self.player_factory(*res) if res else None

    def change_name(self, player: Player, new_name: str) -> Optional[Player]:
        with self.conn:
            self.cur.execute(f"""UPDATE {PlayerTable.TABLE} SET name = ? WHERE name = ? AND id = ?;""", (new_name, player.name, player.id))
            return self.get_player_by_id(player.id)
