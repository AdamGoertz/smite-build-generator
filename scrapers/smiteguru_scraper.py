from bs4 import BeautifulSoup #type: ignore
import requests
from abc import ABC, abstractmethod
from typing import Iterable, Dict, Generator

class Scraper(ABC):
    @abstractmethod
    def builds(self, god_name: str, user:str, id: int, page_range: int):
        pass

class SmiteGuruScraper(Scraper):
    BuildItems = Dict[str, Iterable[str]]

    def __init__(self, item_factory):
        self.item_factory = item_factory

    def builds(self, god_name: str, user: str, id: int, page_range: int) -> Generator[BuildItems, None, None]:
        """Scrapes the HTML for the smite.guru page corresponding to the selected user's matches.

                Parameters:
                    god_name    : str           -> The name of the god you want data_objects for.
                    user        : str           -> The username of the user whose builds you wish to see.
                    id          : int           -> The id of 'user', from the smite.guru url.
                    page_range  : int           -> The # of pages to scrape. More pages takes longer but yields better results.
                Returns:
                    BuildItems -> item and active names for the next build."""

        matches_found = 0
        for i in range(1, page_range+1):
            r = requests.get(f"https://smite.guru/profile/{str(id)}-{user}/matches?page={i}")

            if (r.status_code == 200):
                print(f"searching page ({i}/{page_range}) ...")
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

    