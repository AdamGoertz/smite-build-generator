from filters.filter import Filter, ExclusionFilter, MutualExclusionFilter, DuplicateFilter
from database.config_loader import ItemLoader
from data_objects.item import Item
from typing import List

loader = ItemLoader(Item)
default_item_filters: List[Filter] = []
default_relic_filters: List[Filter] = []

default_item_filters.append(DuplicateFilter())
default_item_filters.append(ExclusionFilter(loader.load("./config/tier_1_items.json")))
default_item_filters.append(ExclusionFilter(loader.load("./config/tier_2_items.json")))
default_item_filters.append(ExclusionFilter(loader.load("./config/blessings.json")))
default_item_filters.append(MutualExclusionFilter(loader.load("./config/masks.json")))
default_item_filters.append(MutualExclusionFilter(loader.load("./config/boots.json")))

default_relic_filters.append(DuplicateFilter())
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/aegis_amulet.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/blink_rune.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/belt_of_frenzy.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/bracer_of_undoing.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/cursed_ankh.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/heavenly_wings.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/horrific_emblem.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/magic_shell.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/meditation_cloak.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/phantom_veil.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/purification_beads.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/shield_of_thorns.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/sundering_spear.json")))
default_relic_filters.append(MutualExclusionFilter(loader.load("./config/teleport_glyph.json")))

