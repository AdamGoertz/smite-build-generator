from filters.item_map import IdentityMap, ItemMap
from database.config_loader import ItemLoader
from data_objects.item import Item
from typing import List

loader = ItemLoader(Item)

default_item_maps: List[ItemMap] = []
default_relic_maps: List[ItemMap] = []

default_item_maps.append(IdentityMap(loader.load("./config/items/book_of_thoth.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/devourer's_gauntlet.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/gauntlet_of_thebes.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/hide_of_the_urchin.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/rage.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/shaman's_ring.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/soul_eater.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/transcendence.json")))
default_item_maps.append(IdentityMap(loader.load("./config/items/warlock's_staff.json")))


default_relic_maps.append(IdentityMap(loader.load("./config/relics/aegis_amulet.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/blink_rune.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/belt_of_frenzy.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/bracer_of_undoing.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/cursed_ankh.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/heavenly_wings.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/horrific_emblem.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/magic_shell.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/meditation_cloak.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/phantom_veil.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/purification_beads.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/shield_of_thorns.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/sundering_spear.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/relics/teleport_glyph.json")))