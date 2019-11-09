from database.connection import SmiteDBConnection
from data_objects.team import Team
from data_objects.player import Player
from database.player_table import PlayerTable
from typing import Tuple

class TeamTable(SmiteDBConnection):
    TABLE = "teams"
    
    def __init__(self, player_table: PlayerTable, team_factory: Team):
        super().__init__()
        self.player_table = player_table
        self.team_factory = team_factory
        self.cur = self.conn.cursor()

        with self.conn as c:
            c.execute(f"""CREATE TABLE IF NOT EXISTS {TeamTable.TABLE} (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          league TEXT,
                          solo INTEGER REFERENCES {self.player_table.TABLE}(id) NOT NULL,
                          jungle INTEGER REFERENCES {self.player_table.TABLE}(id) NOT NULL,
                          mid INTEGER REFERENCES {self.player_table.TABLE}(id) NOT NULL,
                          support INTEGER REFERENCES {self.player_table.TABLE}(id) NOT NULL,
                          adc INTEGER REFERENCES {self.player_table.TABLE}(id) NOT NULL);""")


    def add_team(self, team: Team) -> None:
        with self.conn:
            self.cur.execute(f"""INSERT INTO {TeamTable.TABLE} (name, league, solo, jungle, mid, support, adc)
                                 VALUES (?, ?, ?, ?, ?, ?, ?);""",
                             (team.name, team.league, team.solo.id, team.jungle.id, team.mid.id, team.support.id, team.adc.id))

    def remove_team(self, team: Team) -> None:
        with self.conn:
            self.cur.execute(f"""DELETE FROM {TeamTable.TABLE} WHERE name = ? AND league = ?;""", (team.name, team.league))

    def update_team(self, team: Team, *, old_name="", old_league="") -> None:
        with self.conn:
            self.cur.execute(f"""UPDATE {TeamTable.TABLE} SET 
                                 name = ?,
                                 league = ?,
                                 solo = ?,
                                 jungle = ?,
                                 mid = ?,
                                 support = ?,
                                 adc = ? 
                                 WHERE (name = ? OR name = ?) AND (league = ? OR league = ?);""",
                             (team.name, team.league, team.solo.id, team.jungle.id, team.mid.id, team.support.id, team.adc.id, team.name, old_name, team.league, old_league))

    def get_teams_in_league(self, league: str) -> Tuple[Team]:
        with self.conn:
            self.cur.execute(f"""SELECT * FROM {TeamTable.TABLE}
                                 WHERE league = ?;""", (league,))
            return tuple(self.team_factory(team[1], team[2], *map(self.player_table.get_player_by_id, team[3:])) for team in self.cur.fetchall())

    def get_players_by_role(self, role: str) -> Tuple[Player]:
        if role.lower() not in ("solo", "jungle", "mid", "support", "adc"):
            raise ValueError("Invalid Role")

        with self.conn:
            self.cur.execute(f"""SELECT ({role}) FROM {TeamTable.TABLE};""")
            return tuple(self.player_table.get_player_by_id(player_id[0]) for player_id in self.cur.fetchall())
