from filters.filter import Filter, ExclusionFilter, MutualExclusionFilter, DuplicateExclusionFilter
from database.config_loader import ItemLoader
from data_objects.item import Item
from typing import List

loader = ItemLoader(Item)
default_item_filters: List[Filter] = []
default_relic_filters: List[Filter] = []

default_item_filters.append(DuplicateExclusionFilter())
default_item_filters.append(ExclusionFilter(loader.load("./config/tier_1_items.json")))
default_item_filters.append(ExclusionFilter(loader.load("./config/tier_2_items.json")))
default_item_filters.append(ExclusionFilter(loader.load("./config/blessings.json")))
default_item_filters.append(MutualExclusionFilter(loader.load("./config/masks.json")))
default_item_filters.append(MutualExclusionFilter(loader.load("./config/boots.json")))

default_relic_filters.append(DuplicateExclusionFilter())
#

