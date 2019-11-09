from creators.build_creator import BuildCreator
from scrapers.smiteguru_scraper import Scraper
from data_objects.player import Player
from database.player_table import PlayerTable
from database.team_table import TeamTable

class BuildGenerator:
    def __init__(self, god: str, build_creator: BuildCreator, scraper: Scraper):
        self.build_creator = build_creator
        self.scraper = scraper
        self.god = god

    def track_builds(self, player: Player):
        tracker = self.build_creator.tracker()

        for build in self.scraper.builds(
                self.god,
                player.name,
                player.id
        ):
            tracker.track(build)


class PlayerBuildGenerator(BuildGenerator):
    def __init__(self, god: str, player_name: str, build_creator: BuildCreator, scraper: Scraper, player_data_store: PlayerTable):
        super().__init__(god, build_creator, scraper)
        self.player = player_data_store.get_player_by_name(player_name)


    def generate_build(self):
        self.track_builds(self.player)
        return self.build_creator.get_build()


class RoleBuildGenerator(BuildGenerator):
    def __init__(self, god: str, role: str, build_creator: BuildCreator, scraper: Scraper, player_data_store: PlayerTable, team_data_store: TeamTable):
        super().__init__(god, build_creator, scraper)
        self.role = role
        self.team_data_store = team_data_store

    def track_role_builds(self, role: str):
        players = self.team_data_store.get_players_by_role(self.role)

        for player in players:
            super().track_builds(player)

    def generate_build(self):
        self.track_builds(self.role)
        return self.build_creator.get_build()