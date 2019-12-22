from bs4 import BeautifulSoup #type: ignore
import requests
from abc import ABC, abstractmethod
from typing import Collection, Generator, Type
from data_objects.player import Player
from data_objects.item import Item
from data_objects.build import Build

class BuildDataProvider(ABC):
    @abstractmethod
    def builds(self, god_name: str) -> Generator[Build, None, None]:
        pass

#TODO: Add scraper that keeps searching until a certain number of matches have been found.

class SmiteGuruScraper(BuildDataProvider):
    def __init__(self, item_factory: Type[Item], build_factory: Type[Build], player: Player, *, pages: int=10, verbose: bool=False):
        self.item_factory = item_factory
        self.build_factory = build_factory
        self.user: str = player.name
        self.id: int = player.id
        self.pages = pages
        self.verbose = verbose

    def builds(self, god_name: str) -> Generator[Build, None, None]:
        """Scrapes the HTML for the smite.guru page corresponding to the selected user's matches.

                Parameters:
                    god_name    : str           -> The name of the god you want data_objects for.
                Returns:
                    Build -> item and active names for the next build."""

        if self.verbose:
            print(f"Searching {self.user}'s builds...")

        matches_found = 0
        for i in range(1, self.pages+1):
            r = requests.get(f"https://smite.guru/profile/{str(self.id)}-{self.user}/matches?page={i}")

            if (r.status_code == 200):
                if self.verbose:
                    print(f"Page ({i}/{self.pages})")

                soup = BeautifulSoup(r.text, 'html.parser')

                # A list of all the match widgets in which the target god was played
                matches = [match for match in soup.findAll('div', {'class':'match-widget'}) if match.find('div', {'class':'match-widget--title'}).text == god_name]
                matches_found += len(matches)

                # Collect the item names for each match
                for m in matches:
                    item_tags = m.find('div', {'class' : 'match-widget__items'}).findAll('img')
                    items = tuple(map(self.item_factory, [item.get('alt') for item in item_tags]))
                
                    active_tags = m.find('div', {'class': 'match-widget__actives'}).findAll('img')
                    actives = tuple(map(self.item_factory, [active.get('alt') for active in active_tags]))
                     
                    yield self.build_factory(items, actives)

        if self.verbose:
            print(f"Found {matches_found} {'matches' if matches_found != 1 else 'match'}.")


class MultiPlayerScraper(SmiteGuruScraper):
    def __init__(self, item_factory: Type[Item], build_factory: Type[Build], players: Collection[Player], *, pages: int = 10, verbose: bool=False):
        super().__init__(item_factory, build_factory, next(iter(players)), pages=pages, verbose=verbose)
        self.players = players

    def builds(self, god_name: str) -> Generator[Build, None, None]:
        for player in self.players:
            self.user = player.name
            self.id = player.id
            for build in super().builds(god_name):
                yield build