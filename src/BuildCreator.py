from WeightedGraph import WeightedGraph
from typing import Dict, Any, List

class BuildCreator:
    Build = Dict[str, List[str]]

    def __init__(self, god: str):
        if not isinstance(god, str):
            raise TypeError("god must be a string")

        self.god = god
        self.items = WeightedGraph(label=f"{self.god} - Items")
        self.item_occurrences = {}
        self.active_occurrences = {}
        self.slot_averages = {}
        self.complete_build = {"items" : [], "actives" : []}

    def __str__(self):
        newline_and_tab = "\n\t"
        return f'{self.god}\nItems:\n\t{newline_and_tab.join(self.complete_build["items"])}\nActives:\n\t{newline_and_tab.join(self.complete_build["actives"])}'
        
    def update_slot_average(self, item: str, slot: int, *, item_type: str):
        """Updates slot_averages, active_occurrences, and item_occurrences."""
        if not isinstance(item, str):
            raise TypeError("Invalid item name: must be a string")
        if not isinstance(slot, int):
            raise TypeError("slot must be an integer.")
        if not isinstance(item_type, str):
            raise TypeError("item_type must be a string.")
        elif item_type not in ('item', 'active'):
            raise ValueError("item_type must be either 'item' or 'active'.")
            
        
        avg = self.slot_averages.get(item, 0)
        if item_type == 'item':
            occurrences = self.item_occurrences.get(item, 0) 
        else:
            occurrences = self.active_occurrences.get(item, 0)
        

        total = avg * occurrences
        total += slot
        occurrences += 1
        new_avg = total / occurrences

        self.slot_averages[item] = new_avg
        if item_type == 'item':
            self.item_occurrences[item] = occurrences
        else:
            self.active_occurrences[item] = occurrences


    
    def addBuild(self, build: Build):
        """Adds a build to self.items and self.actives."""
    
        items = build["items"]
        if len(items) > 6:
            raise ValueError("Build contained > 6 items.")
        
        actives = build["actives"]
        if len(actives) > 2:
            raise ValueError("Build contained > 2 actives.")
    

        self.items.loadFromList(items)

        for i, item in enumerate(items):
            self.update_slot_average(item, i, item_type='item')

        for i, active in enumerate(actives):
            self.update_slot_average(active, i, item_type='active')

    
    def get_build(self):
        """Process:
            1) For each item:
                Choose the item that was most frequently built (largest # of co-occurrences) with the items already in the build.
                If there is a tie: choose item with most total occurrences
                For first item: choose most common
            2) Order the items by sorting their slot averages in ascending order.
            3) Get 2 most common actives
        """

        build = []

        # (1)
        for j in range(6):
            best_item = None
            max_freq = 0
            max_occurrences = 0
            for item in self.items.graph:
                # Find the item where the sum of the connections between that item and items in the build is maximized
                freq = sum([self.items.graph.get(item).get(i) for i in self.items.graph.get(item) if (i in build or build == [])])
                # If frequencies are equal, choose item with most total occurrences
                if (freq > max_freq or (freq == max_freq and self.item_occurrences.get(item, 0) > max_occurrences)) and item not in build:
                    best_item = item
                    max_freq = freq
                    max_occurrences = self.item_occurrences.get(best_item)

            build.append(best_item)
            print(f"({j+1}): {build[j]} (Frequency: {self.item_occurrences[build[j]]}) (Slot Avg. {self.slot_averages[build[j]]})")

        # (2)
        build = sorted(build, key=lambda x: self.slot_averages.get(x))
        
        # (3)
        freq_sorted_actives = sorted(self.active_occurrences, key=lambda x: self.active_occurrences.get(x), reverse=True)
        order_sorted_actives = sorted(freq_sorted_actives[:2], key=lambda x: self.slot_averages.get(x))

        self.complete_build["actives"] = order_sorted_actives
        self.complete_build["items"] = build
        return self.complete_build

        

    
