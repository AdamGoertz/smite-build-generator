import sqlite3
from data_objects.team import Team
from typing import Tuple
from dependency_injector.providers import Factory #type: ignore

class TeamTable:
    TABLE = "teams"
    
    def __init__(self, player_table: str, db_conn: sqlite3.Connection, team_factory: Factory):
        self.team_factory = team_factory
        self.conn = db_conn
        self.cur = self.conn.cursor()

        with self.conn as c:
            c.execute(f"""CREATE TABLE IF NOT EXISTS {TeamTable.TABLE} (
                          name PRIMARY KEY,
                          league TEXT,
                          FOREIGN KEY(solo) REFERENCES {player_table}(id) NOT NULL,
                          FOREIGN KEY(jungle) REFERENCES {player_table}(id) NOT NULL,
                          FOREIGN KEY(mid) REFERENCES {player_table}(id) NOT NULL,
                          FOREIGN KEY(support) REFERENCES {player_table}(id) NOT NULL,
                          FOREIGN KEY(ADC) REFERENCES {player_table}(id) NOT NULL                      
                          );""")


    def add_team(self, team: Team) -> None:
        with self.conn:
            self.cur.execute(f"""INSERT INTO {TeamTable.TABLE} (name, league, solo, jungle, mid, support, ADC)
                                 VALUES (?, ?, ?, ?, ?, ?, ?);""",
                             (team.name, team.league, team.solo.id, team.jungle.id, team.mid.id, team.support.id, team.ADC.id))

    def remove_team(self, team: Team) -> None:
        with self.conn:
            self.cur.execute(f"""DELETE FROM {TeamTable.TABLE} WHERE name = ?;""", team.name)

    def update_team(self, team_name: str, team: Team) -> None:
        with self.conn:
            self.cur.execute(f"""UPDATE {TeamTable.TABLE} SET 
                                 name = ?,
                                 league = ?,
                                 solo = ?,
                                 jungle = ?,
                                 mid = ?,
                                 support = ?,
                                 ADC = ? 
                                 WHERE name = ?;""",
                             (team.name, team.league, team.solo.id, team.jungle.id, team.mid.id, team.support.id, team.ADC.id, team_name))

    def get_teams_in_league(self, league: str) -> Tuple[Team]:
        with self.conn:
            self.cur.execute(f"""SELECT * FROM {TeamTable.TABLE}
                                 WHERE league = ?;""", (league,))
            return tuple(self.team_factory(*team) for team in self.cur.fetchall())
