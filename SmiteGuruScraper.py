from bs4 import BeautifulSoup
import requests
from typing import List, Tuple, Dict, Any
import pickle

class SmiteGuruScraper:
    # Custom types, for type hints
    BuildItems = Dict[str, List[str]]
    ItemCodes = Dict[int, str]

    item_codes = {}

    @classmethod
    def getBuildInfo(cls, god_name: str, user: str, id: int, *,  page_range: int =10) -> BuildItems:
        """Scrapes the HTML for the smite.guru page corresponding to the selected user's matches.

                Parameters:
                    god_name    : str           -> The name of the god you want data for.
                    user        : str           -> The username of the user whose builds you wish to see.
                    id          : int           -> The id of 'user', from the smite.guru url.
                    page_range  : int           -> The # of pages to scrape. More pages takes longer but yields better results.
                Returns:
                    BuildItems -> item and active names for the next build."""

        for i in range(1, page_range+1):
            r = requests.get(f"https://smite.guru/profile/{str(id)}-{user}/matches?page={i}")

            if (r.status_code == 200):
                print(f"searching page ({i}/{page_range}) ...")
                soup = BeautifulSoup(r.text, 'html.parser')

                # A list of all the match widgets in which the target god was played
                matches = [match for match in soup.findAll('div', {'class':'match-widget'}) if match.find('div', {'class':'match-widget--title'}).text == god_name] #if match.find(class_="name").string == god_name]
            
                # Collect the item names for each match
                for m in matches:
                    item_tags = m.find('div', {'class' : 'match-widget__items'}).findAll('img')
                    items = [item.get('alt') for item in item_tags]
                
                    active_tags = m.find('div', {'class': 'match-widget__actives'}).findAll('img')
                    actives = [active.get('alt') for active in active_tags]
                     
                    yield {"items" : items, "actives" : actives}

        
    # DEPRECATED SINCE smite.guru REDESIGN
    # @classmethod
    # def getItemCodes(cls):
    #     """Scrapes the HTML for the smite.guru item page, to retrieve the number code which corresponds to each item.

    #             Parameters:
    #                 None
    #             Returns:
    #                 Dict[int : str] -> item_code : item_name
    #     """
    #     r = requests.get("http://smite.guru/items")

    #     if (r.status_code == 200):

    #         soup = BeautifulSoup(r.text, 'html.parser')

    #         # Get listed items
    #         items = soup.findAll(class_="card-icon card-md")
    #         codes_and_names = {int(item["data-item"]) : item.find(class_="name").string for item in items}

    #         # add empty item slot id
    #         codes_and_names[0] = "EMPTY"

    #         cls.item_codes = codes_and_names

    # @classmethod
    # def matchItemCode(cls, item_code: int) -> str:
    #     """Matches an item code to its name.

    #         Parameters:
    #             item_code : int -> the integer code corresponding to an item on smite.guru
    #         Returns:
    #             str -> the name of the item"""

    #     return cls.item_codes[item_code]

    # @classmethod
    # def saveItemCodes(cls, filename: str):
    #     """Saves the scraped item codes to a binary file.

    #         Parameters:
    #             filename : str -> the name of the file
    #         Returns:
    #             None
    #         Throws:
    #             TypeError -> filename was not a string
    #     """

    #     if not isinstance(filename, str):
    #         raise TypeError("filename must be a string.")
    #     pickle.dump(cls.item_codes, open(filename, "wb"))

    # @classmethod
    # def loadItemCodes(cls, filename: str):
    #     """Loads the scraped item codes from a binary file.

    #         Parameters:
    #             filename : str -> the name of the file
    #         Returns:
    #             None
    #         Throws:
    #             TypeError -> filename was not a string
    #     """

    #     if not isinstance(filename, str):
    #         raise TypeError("filename must be a string.")
    #     cls.item_codes = pickle.load(open(filename, "rb"))