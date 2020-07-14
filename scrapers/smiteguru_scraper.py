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
    def __init__(self, item_factory: Type[Item], build_factory: Type[Build], player: Player, *, matches, page_limit, verbose: bool=False):
        self.item_factory = item_factory
        self.build_factory = build_factory
        self.user: str = player.name
        self.id: int = player.id
        self.page_limit = page_limit
        self.matches = matches
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
        page = 1
        while matches_found < self.matches and page <= self.page_limit:
            r = requests.get(f"https://smite.guru/profile/{str(self.id)}-{self.user}/matches?page={page}")

            if (r.status_code == 200):
                if self.verbose:
                    print(f"Page ({page}/{self.page_limit})")

                soup = BeautifulSoup(r.text, 'html.parser')

                # A list of all the match widgets 
                matches = [match for match in soup.findAll('div', {'class':'match-widget'})]

                # If no matches are present on the page, the end of available match history has been reached
                if not matches:
                   raise StopIteration 

                # Find all matches where target god was played
                matches = list(filter(lambda match: match.find('div', {'class':'match-widget--title'}).text == god_name, matches))
                matches_found += len(matches)

                # Collect the items and relics for each match
                for m in matches:
                    item_tags = m.find('div', {'class' : 'match-widget__items'}).findAll('img')
                    items = tuple(map(self.item_factory, [item.get('alt') for item in item_tags]))
                
                    active_tags = m.find('div', {'class': 'match-widget__actives'}).findAll('img')
                    actives = tuple(map(self.item_factory, [active.get('alt') for active in active_tags]))
                     
                    yield self.build_factory(items, actives)
                
            page += 1

        if self.verbose:
            print(f"Found {matches_found} {'matches' if matches_found != 1 else 'match'}.")



class MultiPlayerScraper(SmiteGuruScraper):
    def __init__(self, item_factory: Type[Item], build_factory: Type[Build], players: Collection[Player], *, matches: int, page_limit: int, verbose: bool=False):
        super().__init__(item_factory, build_factory, next(iter(players)), matches=matches, page_limit=page_limit, verbose=verbose)
        self.players: Collection[Player] = players

    def builds(self, god_name: str) -> Generator[Build, None, None]:
        for player in self.players:
            self.user = player.name
            self.id = player.id
            yield from super().builds(god_name)