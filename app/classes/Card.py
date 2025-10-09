from dataclasses import dataclass


@dataclass
class Card:
    def __init__(self, id, name):
        self.id = id
        self.name = name


    def __str__(self):
        return f"{self.name, self.id}"



card = Card(id=4, name="Pikatchu")
print(card)