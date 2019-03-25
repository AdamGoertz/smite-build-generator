from BuildCreator import BuildCreator
from SmiteGuruScraper import SmiteGuruScraper
import argparse

parser = argparse.ArgumentParser(description='Generate a build for a smite god.')
parser.add_argument('god_name', type=str, help='The name of the god to create a build for.')
parser.add_argument('user', type=str, help='The name of the user whose build you want to search.')
parser.add_argument('id', type=int, help='The user id from smite.guru (temporary during development)')
parser.add_argument('-p', type=int, help='page range to search from smite.guru', default=10)
args = parser.parse_args()

if __name__ == '__main__':
    g = SmiteGuruScraper.getBuildInfo(args.god_name, args.user, args.id, page_range=args.p)
    bc = BuildCreator(args.god_name)
    for b in g:
        bc.addBuild(b)

    bc.get_build()
    print(bc)
    
    
