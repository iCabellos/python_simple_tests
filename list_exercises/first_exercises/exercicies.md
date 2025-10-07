# Pokémon TCG – Bloque TRAINER (1–10)

Guía paso a paso en **Python** para levantar los cimientos de un sistema de combate tipo **Pokémon TCG** con **POO**. Cada ejercicio incluye: **Enunciado**, **Descripción breve**, **Objetivos**, y **Ayuda** (enlaces de documentación oficial o recursos fiables).

---

## 1) Tu primera carta (clase mínima)

**Enunciado**: Crea una clase `Card` con atributos `id: str` y `name: str` usando `@dataclass`. Instancia una carta y muéstrala por consola.

**Descripción breve**: Te familiarizas con `dataclasses` para definir objetos inmutables/mutables con poco código.

**Objetivos**:

* Definir una `@dataclass` simple (`Card`).
* Crear una instancia y hacer `print(card)` para verificar su representación.
* (Opcional) Añadir `__post_init__` para validar que `id` y `name` no estén vacíos.

**Ayuda**: [Dataclasses – docs.python.org](https://docs.python.org/3/library/dataclasses.html)

---

## 2) Jerarquía básica de cartas

**Enunciado**: Crea `PokemonCard`, `EnergyCard` y `TrainerCard` que **hereden** de `Card`. Por ahora no añadas campos extra. Crea una instancia de cada una.

**Descripción breve**: Practicas **herencia** para preparar la jerarquía del juego.

**Objetivos**:

* Crear tres subclases de `Card`.
* Instanciar y listar los objetos creados.
* (Opcional) Añadir `__repr__` personalizados.

**Ayuda**: [Clases e herencia – Tutorial oficial](https://docs.python.org/3/tutorial/classes.html#inheritance)

---

## 3) Tipos y salud (HP)

**Enunciado**: Define un `enum Type` (`FIRE`, `WATER`, `GRASS`, `LIGHTNING`, `PSYCHIC`, `FIGHTING`, `COLORLESS`). Añade a `PokemonCard` los campos `type: Type`, `hp_max: int`, `hp_current: int` (inicia igual a `hp_max`).

**Descripción breve**: Introduces **Enum** y atributos específicos en una subclase.

**Objetivos**:

* Crear `enum Type`.
* Extender `PokemonCard` con HP y tipo.
* Asegurar en el constructor que `hp_current = hp_max`.

**Ayuda**: [Enum – docs.python.org](https://docs.python.org/3/library/enum.html)

---

## 4) Ataques básicos

**Enunciado**: Crea `Attack` con `name: str`, `base_damage: int`. Añade `attacks: list[Attack]` a `PokemonCard` y agrega al menos 1 ataque a un Pokémon.

**Descripción breve**: Modelas ataques simples y relación 1:N entre Pokémon y ataques.

**Objetivos**:

* Definir `Attack` como `@dataclass`.
* Añadir una lista de ataques en `PokemonCard` (usa `field(default_factory=list)`).
* (Opcional) Validar que `base_damage >= 0`.

**Ayuda**: [field(default_factory=...) en dataclasses](https://docs.python.org/3/library/dataclasses.html#dataclasses.field)

---

## 5) Energías unidas (contador simple)

**Enunciado**: Crea `EnergyCard` con `etype: Type`. En `PokemonCard`, añade `attached_energy: dict[Type, int]` y una función `attach_energy(pokemon, energy_card)` que incremente el contador.

**Descripción breve**: Representas las energías unidas a un Pokémon con un **diccionario**.

**Objetivos**:

* Definir `EnergyCard(etype: Type)`.
* Añadir `attached_energy` con `default_factory=dict`.
* Implementar `attach_energy(...)` que haga `attached_energy[etype] += 1`.

**Ayuda**: [Diccionarios en Python (tutorial)](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

---

## 6) Daño directo

**Enunciado**: Implementa `apply_damage(pokemon: PokemonCard, amount: int)` que reduzca `hp_current` sin bajar de 0.

**Descripción breve**: Primer contacto con la lógica de **daño** y límites de valores.

**Objetivos**:

* Crear una función que reste HP de forma segura.
* Asegurar `hp_current = max(0, hp_current - amount)`.
* (Opcional) Devolver si el Pokémon ha quedado a 0 (K.O.).

**Ayuda**: [Funciones – Tutorial oficial](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)

---

## 7) Debilidad y resistencia (ajuste de daño)

**Enunciado**: Añade a `PokemonCard`: `weakness: Type | None` (x2 daño) y `resistance: Type | None` (-20 daño, mínimo 0). Crea `compute_damage(attacker, defender, attack)` que aplique estos modificadores sobre `attack.base_damage`.

**Descripción breve**: Extiendes el cálculo de daño con **reglas simples** del TCG.

**Objetivos**:

* Modelar `weakness` y `resistance` opcionales.
* Implementar multiplicador por debilidad (x2) y resta por resistencia (-20, no negativo).
* Devolver el daño final como `int`.

**Ayuda**: [PEP 604 – `X | Y` (tipos unión)](https://peps.python.org/pep-0604/) · [typing – docs](https://docs.python.org/3/library/typing.html)

---

## 8) Banco y Activo

**Enunciado**: Crea `Board` con `active: PokemonCard | None` y `bench: list[PokemonCard]` (máx. 5). Implementa `switch_active(new_active)` que mueva uno del banco a activo (y el activo previo al banco).

**Descripción breve**: Representas el **estado de mesa** básico.

**Objetivos**:

* Definir `Board` con restricciones (banco ≤ 5).
* Validar que `new_active` existe en el banco.
* Intercambiar correctamente activo ↔ banco.

**Ayuda**: [Listas – Tutorial oficial](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

---

## 9) Retirada básica (sin coste)

**Enunciado**: Añade `retreat_to(bench_target)` que realice el **cambio de activo** por un Pokémon del banco sin coste. Reutiliza la lógica de `switch_active`.

**Descripción breve**: Preparas el comportamiento de **retirada** sin todavía aplicar costes.

**Objetivos**:

* Implementar `retreat_to(...)` sobre `Board`.
* Validar que `bench_target` está en el banco.
* Mantener integridad del tamaño del banco tras el intercambio.

**Ayuda**: [Excepciones y validaciones – Tutorial](https://docs.python.org/3/tutorial/errors.html)

---

## 10) Fases y turnos (mínimo viable)

**Enunciado**: Define `Phase` (`START`, `MAIN`, `ATTACK`, `END`) y un `TurnEngine` con `phase` y `next_phase()` que avance cíclicamente por esas fases.

**Descripción breve**: Estructuras el **ciclo de turno** básico del juego.

**Objetivos**:

* Crear `Enum Phase`.
* Implementar `TurnEngine` con `next_phase()` y reinicio tras `END`.
* (Opcional) Hook por fase: métodos vacíos `on_start/on_main/on_attack/on_end`.

**Ayuda**: [Enum – docs.python.org](https://docs.python.org/3/library/enum.html) · [Programación orientada a objetos – Real Python (artículo introductorio)](https://realpython.com/python3-object-oriented-programming/)

---

### Consejos generales

* Usa `from dataclasses import dataclass, field` y `from typing import Optional, Dict, List` para anotar tipos con claridad.
* Pequeños **tests** manuales con `assert` te ayudarán a validar cada paso.
* Mantén los archivos separados si lo prefieres (p. ej., `models.py`, `board.py`, `engine.py`).
