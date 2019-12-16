import argparse
from scrapers.smiteguru_scraper import SmiteGuruScraper
from data_objects.item import Item
from build_generator import PlayerBuildGenerator, RoleBuildGenerator
from trackers.build_tracker import BuildTracker
from trackers.item_tracker import ItemTracker
from graphs.weighted_graph import WeightedGraph
from creators.build_creator import ItemBuildCreator, RelicBuildCreator
from database.player_table import PlayerTable
from database.team_table import TeamTable
from data_objects.player import Player
from data_objects.team import Team

parser = argparse.ArgumentParser(description='get a build for a specific god')
parser.add_argument('god', help='the god to create a build for')
parser.add_argument('--pages', type=int, choices=range(1, 50), required=False, default=10, help='the number of smite.guru pages to search for builds')
build_sources = parser.add_mutually_exclusive_group(required=True)
build_sources.add_argument('--player', help='the player whose builds should be used to create a build')
build_sources.add_argument('--role', help='the role for which a build should be created')

args = parser.parse_args()
ptable = PlayerTable(Player)

scraper = SmiteGuruScraper(Item)
item_graph = WeightedGraph()
relic_graph = WeightedGraph()
item_tracker = BuildTracker(item_graph, ItemTracker)
relic_tracker = BuildTracker(relic_graph, ItemTracker)
item_creator = ItemBuildCreator(item_tracker)
relic_creator = RelicBuildCreator(relic_tracker)

# Player-based search
if args.player:
    generator = PlayerBuildGenerator(args.god, args.player, item_creator, relic_creator, scraper, ptable)
    print(generator.generate_build())

# Role-based search
else:
    ttable = TeamTable(ptable, Team)
    generator = RoleBuildGenerator(args.god, args.role, item_creator, relic_creator, scraper, ptable, ttable)
    print(generator.generate_build())









