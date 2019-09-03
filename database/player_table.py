import sqlite3
from data_objects.player import Player
from typing import Union
from dependency_injector.providers import Factory #type: ignore

class PlayerTable:
    TABLE_NAME = "players"

    def __init__(self, db_conn: sqlite3.Connection, player_factory: Factory):
        self.player_factory = player_factory
        self.conn = db_conn
        self.cur = self.conn.cursor()

        with self.conn as c:
            c.execute(f"""CREATE TABLE IF NOT EXISTS {PlayerTable.TABLE_NAME} (
                      name TEXT NOT NULL,
                      id INTEGER PRIMARY KEY NOT NULL
                      );""")

    def add_player(self, player: Player) -> None:
        with self.conn:
            self.cur.execute(f"""INSERT INTO {PlayerTable.TABLE_NAME} (name, id) VALUES (?, ?);""", (player.name, player.id))

    def remove_player(self, player: Player) -> None:
        with self.conn:
            self.cur.execute(f"""DELETE FROM {PlayerTable.TABLE_NAME} WHERE name = ? AND id = ?;""", (player.name, player.id))

    def get_player_by_name(self, name: str) -> Union[Player, None]:
        # Currently returns only one Player object, even though there may potentially be multiple players with the same name in the database
        with self.conn:
            self.cur.execute(f"""SELECT * FROM {PlayerTable.TABLE_NAME} WHERE name = ?;""", (name,))
            res = self.cur.fetchone()
            return self.player_factory(*res) if res else None

    def get_player_by_id(self, id: int) -> Union[Player, None]:
        with self.conn:
            self.cur.execute(f"""SELECT * FROM {PlayerTable.TABLE_NAME} WHERE id = ?;""", (id,))
            res = self.cur.fetchone()
            return self.player_factory(*res) if res else None

    def change_name(self, player: Player, new_name: str) -> Union[Player, None]:
        with self.conn:
            self.cur.execute(f"""UPDATE {PlayerTable.TABLE_NAME} SET name = ? WHERE name = ? AND id = ?;""", (new_name, player.name, player.id))
            return self.get_player_by_id(player.id)



if __name__ == '__main__':
    conn = sqlite3.connect("smiteuserdb.db")
    pt = PlayerTable(conn, Player)
    player = Player("Test", 12345)
    pt.add_player(player)
    print(pt.get_player_by_name("Test"))
    player = pt.change_name(player, 'NewTest')
    print(player)
    pt.remove_player(player)