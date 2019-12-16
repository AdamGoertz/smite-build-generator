import argparse
from database.player_table import PlayerTable
from database.team_table import TeamTable
from data_objects.player import Player
from data_objects.team import Team

parser = argparse.ArgumentParser(description='Add a new team to the database')
parser.add_argument('--name', help='the team\'s name', required=True)
parser.add_argument('--league', help='the team league', choices=('SPL', 'SML', 'SCL', 'AVGL'), required=True)
parser.add_argument('--solo', help='the team\'s solo laner', required=True)
parser.add_argument('--jungle', help='the team\'s jungler', required=True)
parser.add_argument('--mid', help='the team\'s mid laner', required=True)
parser.add_argument('--support', help='the team\'s support', required=True)
parser.add_argument('--adc', help='the team\'s ADC', required=True)

args = parser.parse_args();

player_table = PlayerTable(Player)
team_table = TeamTable(player_table, Team)

solo = player_table.get_player_by_name(args.solo)
if not solo:
    print(f'Could not find {args.solo} in player table.')

jungle = player_table.get_player_by_name(args.jungle)
if not jungle:
    print(f'Could not find {args.jungle} in player table.')

mid = player_table.get_player_by_name(args.mid)
if not mid:
    print(f'Could not find {args.mid} in player table.')

support = player_table.get_player_by_name(args.support)
if not support:
    print(f'Could not find {args.support} in player table.')

adc = player_table.get_player_by_name(args.adc)
if not adc:
    print(f'Could not find {args.adc} in player table.')

if all((solo, jungle, mid, support, adc)):
    team = Team(args.name, args.league, solo, jungle, mid, support, adc)
    team_table.add_team(team)
