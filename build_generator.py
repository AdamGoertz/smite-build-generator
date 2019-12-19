from creators.build_creator import BuildCreator
from scrapers.smiteguru_scraper import BuildDataProvider

class BuildGenerator:
    def __init__(self, god: str, item_build_creator: BuildCreator, relic_build_creator: BuildCreator, build_data_provider: BuildDataProvider):
        self.item_build_creator = item_build_creator
        self.relic_build_creator = relic_build_creator
        self.build_data_provider = build_data_provider
        self.god = god

    def _track_builds(self):
        item_tracker = self.item_build_creator.tracker()
        relic_tracker = self.relic_build_creator.tracker()

        for build in self.build_data_provider.builds(self.god):
            item_tracker.track(build.get("items"))
            relic_tracker.track(build.get("actives"))

    def generate_build(self):
        self._track_builds()
        return {"Items" : self.item_build_creator.get_build(),
                "Relics" : self.relic_build_creator.get_build()}
