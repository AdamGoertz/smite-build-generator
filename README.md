# smite-build-generator
A tool for scraping smite.guru and generating a suggested item build based on a player's match history.

This tool supports storing players as well as entire teams using a command line interface. To add a new player,
find their player ID from smite.guru and add it to the local database with

```
    python add_player.py --name [player_name] --id [player_id]
```

You can then search their match history for builds using:

```
    python get_build.py [god_name] --player [player_name] (--pages [page_num])
```

In addition to searching by a single player, you can also search based on a conquest role. The intended use of this
feature is to store competitive rosters, then search for common builds across role players from all teams.

For example, you can add a new team to the database like so:

```
    python add_team.py --name [team_name] --league [team_league] --solo [name] --jungle [name] --mid [name]
        --support [name] --adc [name]
```

> *Note:* All players must already be stored in the player table before they can be added to a team.

Then, you can search all the stored teams, and find builds for every role:

```
    python get_build.py [god_name] --role [role_name] (--pages [page_num])
```

Dependencies:
    python 3.7+
    bs4
    requests
