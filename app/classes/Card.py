from dataclasses import dataclass
from enum import Enum
from selectors import SelectSelector
from typing import List
import random


# create enum type
class Phase(Enum):
    START = 1
    MAIN = 2
    ATTACK = 3
    END = 4


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
        self.energy_cost: dict[Type, int] = {}

    def can_pay_attack(self, pokemon):
        for energy_type, required_amount in self.energy_cost.items():
            available = pokemon.attached_energy.get(energy_type, 0)
            if available < required_amount:
                return False
        return True

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
    def __init__(self, id, name, type: Type, hp, resistance: Type, weakness: Type, retreat_cost: int, attacks: list):
        super().__init__(id, name)
        self.type = type
        self.hp = hp
        self.hp_current = self.hp
        self.attacks = attacks
        self.resistance = resistance
        self.weakness = weakness
        self.attached_energy: dict = {}
        self.retreat_cost = retreat_cost

    def can_retreat(self):
        if self.attached_energy.get(Type.COLOURLESS, 0) >= self.retreat_cost:
            return True
        raise Exception("Coste insuficiente")

    def pay_retreat(self):
        if self.can_retreat():
            self.attached_energy[Type.COLOURLESS] -= self.retreat_cost

    def __str__(self):
        return f"{self.name, self.id, self.type, self.hp}"


class Player:
    def __init__(self, id, deck, board):
        self.id: int = id
        self.deck: List[Card] = deck
        self.hand: List[Card] = []
        self.discard: List[Card] = []
        self.board: Board = board

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw(self, amount: int = 1):
        drawn = self.deck[:amount]
        self.hand.extend(drawn)
        del self.deck[:amount]


class EnergyCard(Card):
    def __init__(self, id, name, etype):
        super().__init__(id, name)
        self.etype: Type = etype


class TrainerCard(Card):
    def __init__(self, id: int, name):
        super().__init__(id, name)


class Board:
    def __init__(self, bench: list, active: Card):
        self.bench = bench
        self.active = active
        if not self.validate_bench_board():
            raise ValueError

    def __str__(self):
        return f"{self.active}, {self.bench}"

    def validate_bench_board(self):
        if len(self.bench) > 5:
            return False
        else:
            return True

    def move_to_bench(self, card, index_card=None):
        if self.validate_bench_board():
            self.bench.append(card)
            if index_card is not None:
                self.bench.pop(index_card)
        else:
            raise ValueError

    def switch_active(self, new_active, index_bench_card=None):
        if self.validate_bench_board():
            self.move_to_bench(self.active, index_bench_card)
            self.active = new_active
        else:
            imaginary_slot = self.active
            self.move_to_bench(imaginary_slot, index_bench_card)
            self.active = new_active


class TurnEngine:
    phase = None

    def next_phase(self):
        if self.phase == Phase.END or self.phase is None:
            self.phase = Phase.START
            on_start()
        elif self.phase == Phase.START:
            self.phase = Phase.MAIN
            on_main()
        elif self.phase == Phase.MAIN:
            self.phase = Phase.ATTACK
            on_attack()
        elif self.phase == Phase.ATTACK:
            self.phase = Phase.END
            on_end()


def on_start():
    pass
    # TODO reset de la flag

def on_main():
    pass
# TODO jugar energia, no jugar energia, jugar una energia e intentar jugar otra energia


def on_attack():
    pass


def on_end():
    pass


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
thunder.energy_cost = {Type.LIGHTNING: 2, Type.COLOURLESS: 1}
metal_arms = Attack(id=8, name="Metal Arms", base_damage=20)
metal_arms.energy_cost = {Type.STEEL: 1}
rock_tomb = Attack(id=8, name="Rock Tomb", base_damage=50)
pokemonCard = PokemonCard(id=5, name="Pikachu", type=Type.LIGHTNING, hp=60, attacks=[thunder], weakness=Type.FIGHTING,
                          resistance=Type.LIGHTNING, retreat_cost=1)
pokemon2Card = PokemonCard(id=5, name="Skarmory", type=Type.STEEL, hp=120, attacks=[metal_arms],
                           weakness=Type.LIGHTNING,
                           resistance=Type.FIGHTING, retreat_cost=2)
pokemon3Card = PokemonCard(id=5, name="Onyx", type=Type.FIGHTING, hp=120, attacks=[rock_tomb], weakness=Type.GRASS,
                           resistance=Type.NONE, retreat_cost=4)
energyCard = EnergyCard(id=6, name="Colourless", etype=Type.COLOURLESS)
trainerCard = TrainerCard(id=7, name="Potion")

pokemonCard.attached_energy = {Type.COLOURLESS: 4, Type.LIGHTNING: 3}
pokemon2Card.attached_energy = {Type.COLOURLESS: 1}

pokemonlist = [pokemon2Card]
pokemon2list = [pokemonCard, pokemon3Card, pokemon2Card, pokemon3Card, pokemon2Card]

print(thunder.can_pay_attack(pokemonCard))
print(metal_arms.can_pay_attack(pokemon2Card))
turn_engine = TurnEngine()
