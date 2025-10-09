from dataclasses import dataclass


@dataclass
class Card:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.name, self.id}"


class PokemonCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)


class EnergyCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)


class TrainerCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)


pokemonCard = PokemonCard(id=5, name="Pikachu")
energyCard = EnergyCard(id=6, name="Fire")
trainerCard = TrainerCard(id=7, name="Potion")
print(pokemonCard)
print(energyCard)
print(trainerCard)
