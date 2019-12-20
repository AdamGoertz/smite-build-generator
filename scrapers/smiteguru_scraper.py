from bs4 import BeautifulSoup #type: ignore
import requests
from abc import ABC, abstractmethod
from typing import Iterable, Sequence, Dict, Generator, Type
from data_objects.player import Player
from data_objects.item import Item

class BuildDataProvider(ABC):
    BuildItems = Dict[str, Iterable[Item]]

    @abstractmethod
    def builds(self, god_name: str) -> Generator[BuildItems, None, None]:
        pass

class SmiteGuruScraper(BuildDataProvider):
    def __init__(self, item_factory: Type[Item], player: Player, pages: int = 10):
        self.item_factory = item_factory
        self.user = player.name
        self.id = player.id
        self.pages = pages;

    def builds(self, god_name: str) -> Generator[BuildDataProvider.BuildItems, None, None]:
        """Scrapes the HTML for the smite.guru page corresponding to the selected user's matches.

                Parameters:
                    god_name    : str           -> The name of the god you want data_objects for.
                Returns:
                    BuildItems -> item and active names for the next build."""

        matches_found = 0
        for i in range(1, self.pages+1):
            r = requests.get(f"https://smite.guru/profile/{str(self.id)}-{self.user}/matches?page={i}")

            if (r.status_code == 200):
                print(f"searching page ({i}/{self.pages}) ...")
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
                     
                    yield {"items" : items, "actives" : actives}


class MultiPlayerScraper(SmiteGuruScraper):
    def __init__(self, item_factory: Type[Item], players: Sequence[Player], pages: int = 10):
        super().__init__(item_factory, players[0], pages)
        self.players = players

    def builds(self, god_name: str):
        for player in self.players:
            super().user = player.name
            super().id = player.id
            for build in super().builds(god_name):
                yield build