from dataclasses import dataclass

@dataclass(frozen=True)
class Item:
    name: str

    def __str__(self):
        return self.name