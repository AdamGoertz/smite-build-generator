# smite-build-generator
A tool for scraping smite.guru and generating a suggested item build based on a player's match history.

Usage: The script can be run from the command line using 
```
    python main.py [god_name] [user] [user-id] (-p [page-range])
```

Dependencies: 
    python 3.5+
    bs4
    requests
    argparse
    pickle
