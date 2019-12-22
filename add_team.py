import argparse
from database.player_table import PlayerTable
from database.team_table import TeamTable
from data_objects.player import Player
from data_objects.team import Team

parser = argparse.ArgumentParser(description='Add a new team to the database')
parser.add_argument('--name', help='the team\'s name', required=True)
parser.add_argument('--league', help='the team league', choices=('SPL', 'SML', 'SCL', 'AVGL'), required=True)
parser.add_argument('--solo', help='the team\'s solo laner', required=False, default=None)
parser.add_argument('--jungle', help='the team\'s jungler', required=False, default=None)
parser.add_argument('--mid', help='the team\'s mid laner', required=False, default=None)
parser.add_argument('--support', help='the team\'s support', required=False, default=None)
parser.add_argument('--adc', help='the team\'s ADC', required=False, default=None)

args = parser.parse_args()

player_table = PlayerTable(Player)
team_table = TeamTable(player_table, Team)

solo = player_table.get_player_by_name(args.solo) if args.solo else None
if args.solo and not solo:
    print(f'Could not find {args.solo} in player table.')

jungle = player_table.get_player_by_name(args.jungle) if args.jungle else None
if args.jungle and not jungle:
    print(f'Could not find {args.jungle} in player table.')

mid = player_table.get_player_by_name(args.mid) if args.mid else None
if args.mid and not mid:
    print(f'Could not find {args.mid} in player table.')

support = player_table.get_player_by_name(args.support) if args.support else None
if args.support and not support:
    print(f'Could not find {args.support} in player table.')

adc = player_table.get_player_by_name(args.adc) if args.adc else None
if args.adc and not adc:
    print(f'Could not find {args.adc} in player table.')

team = Team(args.name, args.league, solo, jungle, mid, support, adc)
team_table.add_team(team)
