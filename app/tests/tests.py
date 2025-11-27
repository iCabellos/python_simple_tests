from logging import raiseExceptions

import pytest
from app.classes.Card import PokemonCard, Type, apply_damage, EnergyCard
# -----------------------------
# TESTS
# -----------------------------

def test_can_retreat_with_exact_energy():
    """Debe permitir retirada cuando hay exactamente el coste requerido."""
    card = PokemonCard(1, "Testmon", Type.COLOURLESS, 50, None, None, 2, [])
    card.attached_energy = {Type.COLOURLESS: 2}

    assert card.can_retreat() is True


def test_can_retreat_with_more_energy():
    """Debe permitir retirada cuando hay más energía de la necesaria."""
    card = PokemonCard(1, "Testmon", Type.COLOURLESS, 50, None, None, 1, [])
    card.attached_energy = {Type.COLOURLESS: 3}

    assert card.can_retreat() is True


def test_cannot_retreat_with_less_energy():
    """Debe impedir retirada si no hay suficiente energía."""
    card = PokemonCard(1, "Testmon", Type.COLOURLESS, 50, None, None, 3, [])
    card.attached_energy = {Type.COLOURLESS: 1}

    with pytest.raises(Exception, match="Coste insuficiente"):
        card.can_retreat()



def test_cannot_retreat_without_colourless_energy():
    """Debe impedir retirada si no hay energía incolora asignada."""
    card = PokemonCard(1, "Testmon", Type.COLOURLESS, 50, None, None, 2, [])
    card.attached_energy = {}  # Nada asignado

    with pytest.raises(Exception, match="Coste insuficiente"):
        card.can_retreat()


def test_cannot_retreat_when_colourless_key_exists_but_is_none():
    """Caso defensivo: clave existe pero su valor está a None."""
    card = PokemonCard(1, "Testmon", Type.COLOURLESS, 50, None, None, 1, [])
    card.attached_energy = {Type.COLOURLESS: None}

    # None >= 1 daría error, por lo que se espera False
    with pytest.raises(TypeError):
        card.can_retreat()


def test_cannot_retreat_when_colourless_key_is_zero():
    """Debe impedir retirada si hay 0 energías incoloras."""
    card = PokemonCard(1, "Testmon", Type.COLOURLESS, 50, None, None, 1, [])
    card.attached_energy = {Type.COLOURLESS: 0}

    with pytest.raises(Exception, match="Coste insuficiente"):
        card.can_retreat()

def test_apply_damage_reduces_hp():
    card = PokemonCard(1, "Testmon", Type.GRASS, 100, None, None, 1, [])
    card.hp_current = 100

    result = apply_damage(card, 30)
    assert result == 70


def test_apply_damage_never_negative():
    card = PokemonCard(1, "Testmon", Type.GRASS, 100, None, None, 1, [])
    card.hp_current = 10

    result = apply_damage(card, 50)
    assert result == 0

def test_attached_energy_add_first_energy_type():
    """Debe registrar correctamente una energía nueva en el diccionario."""
    card = PokemonCard(1, "Testmon", Type.GRASS, 50, None, None, 1, [])
    card.attached_energy = {}

    card.attached_energy[Type.FIRE] = 1

    assert card.attached_energy == {Type.FIRE: 1}


def test_attached_energy_increment_existing_type():
    """Debe sumar energías correctamente cuando ya existe la clave."""
    card = PokemonCard(1, "Testmon", Type.GRASS, 50, None, None, 1, [])
    card.attached_energy = {Type.COLOURLESS: 1}

    card.attached_energy[Type.COLOURLESS] += 1

    assert card.attached_energy[Type.COLOURLESS] == 2


def test_attached_energy_multiple_types():
    """Debe permitir múltiples tipos de energía simultáneamente."""
    card = PokemonCard(1, "Testmon", Type.GRASS, 50, None, None, 1, [])
    card.attached_energy = {
        Type.FIRE: 2,
        Type.GRASS: 1,
        Type.COLOURLESS: 3
    }

    assert card.attached_energy[Type.FIRE] == 2
    assert card.attached_energy[Type.GRASS] == 1
    assert card.attached_energy[Type.COLOURLESS] == 3




