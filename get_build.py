import argparse
from filters import default_filters, default_maps
from creators.build_creator import ItemBuildCreator, RelicBuildCreator
from data_objects.build import Build
from data_objects.item import Item
from data_objects.player import Player
from data_objects.team import Team
from database.player_table import PlayerTable
from database.team_table import TeamTable
from generators.build_generator import BuildGenerator
from graphs.weighted_graph import WeightedGraph
from scrapers.smiteguru_scraper import SmiteGuruScraper, MultiPlayerScraper
from trackers.build_tracker import BuildTracker
from trackers.item_tracker import ItemTracker

parser = argparse.ArgumentParser(description='get a build for a specific god')
parser.add_argument('god', help='the god to create a build for')
parser.add_argument('--pages', type=int, choices=range(1, 50), required=False, default=10, help='the number of smite.guru pages to search for builds')
parser.add_argument('--verbose', action="store_true", help='print debug messages while generating the build')
build_sources = parser.add_mutually_exclusive_group(required=True)
build_sources.add_argument('--player', help='the player whose builds should be used to create a build')
build_sources.add_argument('--role', help='the role for which a build should be created')

args = parser.parse_args()
ptable = PlayerTable(Player)

item_graph = WeightedGraph()
relic_graph = WeightedGraph()
item_tracker = BuildTracker(item_graph, ItemTracker, default_maps.default_item_maps)
relic_tracker = BuildTracker(relic_graph, ItemTracker, default_maps.default_relic_maps)
item_creator = ItemBuildCreator(default_filters.default_item_filters)
relic_creator = RelicBuildCreator(default_filters.default_relic_filters)

# Player-based search
if args.player:
    player = ptable.get_player_by_name(args.player)
    if player:
        scraper = SmiteGuruScraper(Item, Build, player, pages=args.pages, verbose=args.verbose)
        generator = BuildGenerator(args.god, Build, item_tracker, relic_tracker, item_creator, relic_creator, scraper)
        print(generator.generate_build())
    else:
        print(f'{args.player} was not found in the database.')

# Role-based search
else:
    ttable = TeamTable(ptable, Team)
    players = ttable.get_players_by_role(args.role)
    if players:
        scraper = MultiPlayerScraper(Item, Build, players, pages=args.pages, verbose=args.verbose)
        generator = BuildGenerator(args.god, Build, item_tracker, relic_tracker, item_creator, relic_creator, scraper)
        print(generator.generate_build())
    else:
        print(f'No players with role "{args.role}" found in database.')









