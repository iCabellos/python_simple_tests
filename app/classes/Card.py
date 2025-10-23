from dataclasses import dataclass
from enum import Enum


# create enum type

class Type(Enum):
    FIRE = 1
    WATER = 2
    GRASS = 3
    LIGHTNING = 4
    PSYCHIC = 5
    FIGHTING = 6
    COLOURLESS = 7

class Attack:
    def __init__(self, id, name, base_damage):
        self.id = id
        self.name: str = name
        self.base_damage: int = base_damage
        self.validate_based_damage()

    def __str__(self):
        return f"{self.name, self.id, self.base_damage}"

    def validate_based_damage(self):
        if self.base_damage < 0:
            raise ValueError("Daño base inválido")


@dataclass
class Card:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.name, self.id}"


class PokemonCard(Card):
    def __init__(self, id, name, type, hp, attacks: list):
        super().__init__(id, name)
        self.type = type
        self.hp = hp
        self.hp_current = self.hp
        self.attacks = attacks
        self.attached_energy: dict = {}

    def __str__(self):
        return f"{self.name, self.id, self.type, self.hp}"


class EnergyCard(Card):
    def __init__(self, id, name, etype):
        super().__init__(id, name)
        self.etype:Type = etype


class TrainerCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)

def attach_energy(pokemon: PokemonCard, energy_card: EnergyCard):
    if energy_card.etype not in pokemon.attached_energy:
        pokemon.attached_energy[energy_card.etype] = 0
    pokemon.attached_energy[energy_card.etype] += 1
    print(pokemon.attached_energy)


rayo = Attack(id=8, name="Rayo", base_damage=100)
pokemonCard = PokemonCard(id=5, name="Pikachu", type=Type.LIGHTNING, hp=100, attacks=[rayo])
energyCard = EnergyCard(id=6, name="Colourless", etype=Type.COLOURLESS)
trainerCard = TrainerCard(id=7, name="Potion")
print(pokemonCard)
print(energyCard)
print(trainerCard)
