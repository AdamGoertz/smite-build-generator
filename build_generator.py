from creators.build_creator import BuildCreator
from scrapers.smiteguru_scraper import Scraper
from data_objects.player import Player
from database.player_table import PlayerTable
from database.team_table import TeamTable

class BuildGenerator:
    def __init__(self, god: str, item_build_creator: BuildCreator, relic_build_creator: BuildCreator, scraper: Scraper):
        self.item_build_creator = item_build_creator
        self.relic_build_creator = relic_build_creator
        self.scraper = scraper
        self.god = god

    def track_builds(self, player: Player, page_range: int = 10):
        item_tracker = self.item_build_creator.tracker()
        relic_tracker = self.relic_build_creator.tracker()

        for build in self.scraper.builds(
                self.god,
                player.name,
                player.id,
                page_range
        ):
            item_tracker.track(build.get("items"))
            relic_tracker.track(build.get("actives"))


class PlayerBuildGenerator(BuildGenerator):
    def __init__(self, god: str, player_name: str, item_build_creator: BuildCreator, relic_build_creator: BuildCreator, scraper: Scraper, player_data_store: PlayerTable):
        super().__init__(god, item_build_creator, relic_build_creator, scraper)
        self.player = player_data_store.get_player_by_name(player_name)

    def generate_build(self):
        self.track_builds(self.player)
        return {"Items" : self.item_build_creator.get_build(),
                "Relics" : self.relic_build_creator.get_build()}


class RoleBuildGenerator(BuildGenerator):
    def __init__(self, god: str, role: str, item_build_creator: BuildCreator, relic_build_creator: BuildCreator, scraper: Scraper, player_data_store: PlayerTable, team_data_store: TeamTable):
        super().__init__(god, item_build_creator, relic_build_creator, scraper)
        self.role = role
        self.team_data_store = team_data_store

    def track_role_builds(self, role: str, page_range: int = 10):
        players = self.team_data_store.get_players_by_role(self.role)

        for player in players:
            super().track_builds(player, page_range)

    def generate_build(self):
        self.track_builds(self.role)
        return {"Items": self.item_build_creator.get_build(),
                "Relics": self.relic_build_creator.get_build()}