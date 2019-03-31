from math import fabs
from WeightedGraph import WeightedGraph
from typing import Dict, Any, List

class BuildCreator:
    Build = Dict[str, List[str]]

    def __init__(self, god: str):
        if not isinstance(god, str):
            raise TypeError("god must be a string")

        self.god = god
        self.items = WeightedGraph(label=f"{self.god} - Items")
        self.matches_recorded = 0
        self.item_occurrences = {}
        self.active_occurrences = {}
        self.slot_averages = {}
        self.slot_variance = {}
        self.complete_build = {"items" : [], "actives" : []}

    def __str__(self):
        if self.matches_recorded > 0:
            warning_message = "WARNING: Not enough matches found -- results may be inaccurate.\n"
            return (f'{warning_message if self.matches_recorded <= 5 else ""}'
                    f'~~~{self.god}~~~\n'
                    'Items:\n'
                    f'  1. {self.complete_build["items"][0]}\n'
                    f'  2. {self.complete_build["items"][1]}\n'
                    f'  3. {self.complete_build["items"][2]}\n'
                    f'  4. {self.complete_build["items"][3]}\n'
                    f'  5. {self.complete_build["items"][4]}\n'
                    f'  6. {self.complete_build["items"][5]}\n'
                    'Relics:\n'
                    f'  1. {self.complete_build["actives"][0]}\n'
                    f'  2. {self.complete_build["actives"][1]}\n'
                    )
        else:
            return "No matches analyzed."

    def update_slot_average(self, item: str, slot: int, *, item_type: str):
        """Updates slot_averages and either active_occurrences or item_occurrences."""
            
        slot_avg = self.slot_averages.get(item, 0)
        var_avg = self.slot_variance.get(item, 0)

        if item_type == 'item':
            occurrences = self.item_occurrences.get(item, 0) 
        else:
            occurrences = self.active_occurrences.get(item, 0)

        # Compute the new average item slot
        total = slot_avg * occurrences
        total += slot
        new_avg = total / (occurrences + 1)

        # Compute the new average variance in item slot
        total_var = var_avg * occurrences
        total_var += fabs(new_avg - slot)
        new_var = total_var / (occurrences + 1)

        occurrences += 1
        
        self.slot_averages[item] = new_avg
        self.slot_variance[item] = new_var
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

        self.matches_recorded += 1

    
    def get_build(self):
        """Process:
            1) For each item:
                Choose the item that was most frequently built (largest # of co-occurrences) with the items already in the build.
                If there is a tie: choose item with most total occurrences
                For first item: choose most common
            2) Get 2 most common actives
            3) Order the items & actives by sorting their slot averages in ascending order.
               High variance moves items farther back in build if their average slot is high, 
               but moves them up in the order if their average slot is low.
        """

        if self.matches_recorded == 0:
            return None

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
            print((f"({j+1}): "
                   f"{best_item:<27} "
                   f"(Freq. {max_occurrences/self.matches_recorded:<4.2f}) "
                   f"(Mut Freq. {(max_freq/(self.matches_recorded*j) if j > 0 else 1):<4.2f}) "
                   f"(Slot {(self.slot_averages[best_item]):<5.2f}) "
                   f"(Slot Var. {self.slot_variance[best_item]:<5.2f})"
                   ))

        # (2)
        freq_sorted_actives = sorted(self.active_occurrences, key=lambda x: self.active_occurrences.get(x), reverse=True)
        
        # (3) 
        build = sorted(build, key=lambda x: (self.slot_averages.get(x))+(self.slot_variance.get(x) if self.slot_averages.get(x) >= 2.5 else -1*self.slot_variance.get(x)))
        order_sorted_actives = sorted(freq_sorted_actives[:2], key=lambda x: self.slot_averages.get(x))

        self.complete_build["actives"] = order_sorted_actives
        self.complete_build["items"] = build
        return self.complete_build

        

    
