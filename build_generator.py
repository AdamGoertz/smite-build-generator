from creators.build_creator import BuildCreator
from scrapers.smiteguru_scraper import BuildDataProvider
from data_objects.build import Build
from typing import Type

class BuildGenerator:
    def __init__(self,
                 god: str,
                 build_factory: Type[Build],
                 item_build_creator: BuildCreator,
                 relic_build_creator: BuildCreator,
                 build_data_provider: BuildDataProvider):
        self.build_factory = build_factory
        self.item_build_creator = item_build_creator
        self.relic_build_creator = relic_build_creator
        self.build_data_provider = build_data_provider
        self.god = god

    def _track_builds(self):
        item_tracker = self.item_build_creator.tracker()
        relic_tracker = self.relic_build_creator.tracker()

        for build in self.build_data_provider.builds(self.god):
            item_tracker.track(build.items)
            relic_tracker.track(build.relics)

    def generate_build(self):
        self._track_builds()
        return self.build_factory(self.item_build_creator.get_build(), self.relic_build_creator.get_build())
