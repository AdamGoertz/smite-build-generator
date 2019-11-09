import argparse
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








