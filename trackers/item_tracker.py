from data.item import Item
from typing import Dict

class ItemTracker:
    def  __init__(self, item: Item):
        self.item = item
        self.count: int = 0
        self.slots: Dict[int, int] = {}

    def track(self, slot: int):
        self.slots[slot] = self.slots.get(slot, 0) + 1
        self.count += 1

    def get_slots(self):
        return sorted(list(filter(lambda k: self.slots.get(k, 0) != 0, self.slots.keys())), key=lambda k: self.slots.get(k), reverse=True)

    def __repr__(self):
        return f"{self.item}({self.count}){self.get_slots()}"