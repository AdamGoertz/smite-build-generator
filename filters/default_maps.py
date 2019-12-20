from filters.map import IdentityMap, Map
from database.config_loader import ItemLoader
from data_objects.item import Item
from typing import List

loader = ItemLoader(Item)

default_item_maps: List[Map] = []
default_relic_maps: List[Map] = []

default_item_maps.append(IdentityMap(loader.load("./config/book_of_thoth.json")))
default_item_maps.append(IdentityMap(loader.load("./config/devourer's_gauntlet.json")))
default_item_maps.append(IdentityMap(loader.load("./config/gauntlet_of_thebes.json")))
default_item_maps.append(IdentityMap(loader.load("./config/hide_of_the_urchin.json")))
default_item_maps.append(IdentityMap(loader.load("./config/rage.json")))
default_item_maps.append(IdentityMap(loader.load("./config/shaman's_ring.json")))
default_item_maps.append(IdentityMap(loader.load("./config/soul_eater.json")))
default_item_maps.append(IdentityMap(loader.load("./config/transcendence.json")))
default_item_maps.append(IdentityMap(loader.load("./config/warlock's_staff.json")))


default_relic_maps.append(IdentityMap(loader.load("./config/aegis_amulet.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/blink_rune.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/belt_of_frenzy.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/bracer_of_undoing.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/cursed_ankh.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/heavenly_wings.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/horrific_emblem.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/magic_shell.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/meditation_cloak.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/phantom_veil.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/purification_beads.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/shield_of_thorns.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/sundering_spear.json")))
default_relic_maps.append(IdentityMap(loader.load("./config/teleport_glyph.json")))