from BuildCreator import BuildCreator
from SmiteGuruScraper import SmiteGuruScraper

if __name__ == '__main__':
    god_name = "Jormungandr"
    g = SmiteGuruScraper.getBuildInfo(god_name, "Wlfy", 873380, page_range=7)
    bc = BuildCreator(god_name)
    for b in g:
        bc.addBuild(b)

    bc.get_build()
    print(bc)
    
    
