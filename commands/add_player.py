import argparse
from database.player_table import PlayerTable
from data_objects.player import Player

parser = argparse.ArgumentParser(description='Add a new player to the database')
parser.add_argument('--name', help='the player\'s name', required=True)
parser.add_argument('--id', type=int, help='the player\'s id', required=True)

args = parser.parse_args();

player = Player(args.name, args.id)

table = PlayerTable(Player)

table.add_player(player)


