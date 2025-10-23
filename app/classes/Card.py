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
    NONE = 8
    STEEL = 9


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
    def __init__(self, id, name, type: Type, hp, resistance: Type, weakness: Type, attacks: list):
        super().__init__(id, name)
        self.type = type
        self.hp = hp
        self.hp_current = self.hp
        self.attacks = attacks
        self.resistance = resistance
        self.weakness = weakness
        self.attached_energy: dict = {}

    def __str__(self):
        return f"{self.name, self.id, self.type, self.hp}"


class EnergyCard(Card):
    def __init__(self, id, name, etype):
        super().__init__(id, name)
        self.etype: Type = etype


class TrainerCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)


def attach_energy(pokemon: PokemonCard, energy_card: EnergyCard):
    if energy_card.etype not in pokemon.attached_energy:
        pokemon.attached_energy[energy_card.etype] = 0
    pokemon.attached_energy[energy_card.etype] += 1
    print(pokemon.attached_energy)

def apply_damage(pokemon: PokemonCard, base_damage: int):
    return max(0, pokemon.hp_current - base_damage)

def compute_damage(attacker: PokemonCard, defender: PokemonCard, attack: Attack):
    if attacker.type.value == defender.weakness.value:
        real_damage = attack.base_damage * 2
        return apply_damage(defender, real_damage)
    elif attacker.type.value == defender.resistance.value:
        real_damage = attack.base_damage - 20
        return apply_damage(defender, real_damage)

    return apply_damage(defender, attack.base_damage)

thunder = Attack(id=8, name="Thunder", base_damage=80)
metal_arms = Attack(id=8, name="Metal Arms", base_damage=20)
rock_tomb = Attack(id=8, name="Rock Tomb", base_damage=50)
pokemonCard = PokemonCard(id=5, name="Pikachu", type=Type.LIGHTNING, hp=60, attacks=[thunder], weakness=Type.FIGHTING,
                          resistance=Type.LIGHTNING)
pokemon2Card = PokemonCard(id=5, name="Skarmory", type=Type.STEEL, hp=120, attacks=[metal_arms], weakness=Type.LIGHTNING,
                          resistance=Type.FIGHTING)
pokemon3Card = PokemonCard(id=5, name="Onyx", type=Type.FIGHTING, hp=120, attacks=[rock_tomb], weakness=Type.GRASS,
                          resistance=Type.NONE)
energyCard = EnergyCard(id=6, name="Colourless", etype=Type.COLOURLESS)
trainerCard = TrainerCard(id=7, name="Potion")
print(compute_damage(pokemon3Card, pokemon2Card, pokemon3Card.attacks[0]))
