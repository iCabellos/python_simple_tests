# Pokémon TCG – Bloque JUNIOR (11–20)

Segundo bloque en **Python** para seguir construyendo el sistema de combate tipo **Pokémon TCG**. Cada ejercicio incluye: **Enunciado**, **Descripción breve**, **Objetivos**, y **Ayuda**.

---

## 11) Coste de retirada (en Colorless)

**Enunciado**: Añade a `PokemonCard` el campo `retreat_cost: int` (coste en Colorless). Implementa `can_retreat(pokemon)` que verifique si `attached_energy.get(Type.COLORLESS, 0) >= retreat_cost`.

**Descripción breve**: Empiezas a restringir acciones con **costes** pagables mediante energías unidas.

**Objetivos**:

* Campo `retreat_cost` en `PokemonCard` (por defecto 0–2).
* Función `can_retreat(pokemon)` que devuelva `bool`.
* Tests con casos válidos e inválidos.

**Ayuda**: [dict.get – Documentación](https://docs.python.org/3/library/stdtypes.html#dict.get)

---

## 12) Pago de retirada (descarga de energías)

**Enunciado**: Implementa `pay_retreat(pokemon)` que descuente `retreat_cost` de energías Colorless en `attached_energy`. Integra el pago en `board.retreat_to(bench_target)`.

**Descripción breve**: Añades **mutación controlada** del estado al pagar costes.

**Objetivos**:

* Validar con `can_retreat` antes de pagar.
* Descontar exactamente el coste (no negativo).
* Lanzar una excepción clara si no alcanza.

**Ayuda**: [Excepciones – Tutorial](https://docs.python.org/3/tutorial/errors.html)

---

## 13) Coste de ataque por tipos de energía

**Enunciado**: Amplía `Attack` con `energy_cost: dict[Type,int]` (p.ej., `{Type.FIRE:1, Type.COLORLESS:1}`). Implementa `can_pay_attack(pokemon, attack)` y `pay_attack(pokemon, attack)`.

**Descripción breve**: Introduces pagos por **múltiples tipos** de energía.

**Objetivos**:

* Definir el coste en el modelo `Attack`.
* Verificar disponibilidad de cada tipo requerido.
* Descontar energías al atacar.

**Ayuda**: [typing.Dict](https://docs.python.org/3/library/typing.html#typing.Dict) · [dataclasses.field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field)

---

## 14) Baraja, mano y descarte

**Enunciado**: Crea `Player` con `deck: list[Card]`, `hand: list[Card]`, `discard: list[Card]`, `board: Board`. Implementa `shuffle_deck(player)` y `draw(player, n)`.

**Descripción breve**: Modelas los **zones** principales del TCG.

**Objetivos**:

* Barajar con `random.shuffle`.
* Robar `n` cartas moviéndolas de `deck` → `hand`.
* Respetar orden LIFO o definición propia consistente.

**Ayuda**: [random.shuffle](https://docs.python.org/3/library/random.html#random.shuffle) · [Listas](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

---

## 15) Una energía por turno

**Enunciado**: Añade en `Player` un flag `attached_energy_this_turn: bool`. Implementa `attach_energy_to(player, pokemon, energy_card)` que sólo permita **1 energía por turno** y resetea el flag al cambiar de turno.

**Descripción breve**: Implementas una **regla de turno** básica.

**Objetivos**:

* Flag en `Player` con valor inicial `False`.
* Validación antes de adjuntar energía.
* Reset del flag al finalizar/cambiar turno.

**Ayuda**: [Atributos y estado de instancia](https://docs.python.org/3/tutorial/classes.html#random-remarks)

---

## 16) Evolución básica

**Enunciado**: Crea `EvolutionStage` (`BASIC`, `STAGE1`, `STAGE2`) y campos `stage: EvolutionStage`, `previous_names: list[str]` en `PokemonCard`. Implementa `evolve(basic, stage1)` preservando energías, daño y estados (ajustando `hp_current` al nuevo `hp_max` si fuera necesario).

**Descripción breve**: Manejas **sustitución** de objetos manteniendo propiedades acumuladas.

**Objetivos**:

* Validar que el nombre previo concuerde (p.ej., `stage1.previous_names` contiene `basic.name`).
* Transferir `attached_energy`, daño y estados.
* Reemplazar la carta en `board.active` o en `bench`.

**Ayuda**: [Enum](https://docs.python.org/3/library/enum.html) · [copy/deepcopy](https://docs.python.org/3/library/copy.html)

---

## 17) K.O. y cartas de Premio (Prizes)

**Enunciado**: Cuando un Pokémon llega a `hp_current == 0`, márcalo como **K.O.** y muévelo a `discard`. Implementa `player.prizes: list[Card]` (6 por defecto). Al dejar K.O. al rival, roba 1 prize a tu mano.

**Descripción breve**: Añades **condiciones de victoria** parciales y cambios de zona.

**Objetivos**:

* Evento de K.O. que mueve la carta correctamente.
* Robo de 1 prize a mano del jugador que causa el K.O.
* Comprobar condición de victoria por premios agotados.

**Ayuda**: [Control de flujo y `assert`](https://docs.python.org/3/tutorial/controlflow.html) · [List slicing](https://docs.python.org/3/tutorial/introduction.html#lists)

---

## 18) Cartas Trainer: Item (un solo uso)

**Enunciado**: En `TrainerCard`, añade `kind: Literal["Item","Supporter","Stadium"]`. Implementa `play_item(player, item)` que ejecute su efecto (p.ej., `Potion`: cura 20 al Activo) y envíe la carta a `discard`.

**Descripción breve**: Modelas **cartas de efecto inmediato**.

**Objetivos**:

* Diferenciar tipos de Trainer con `Literal` o `Enum`.
* Implementar al menos 2 Items (p.ej., `Potion`, `Switch`).
* Validar que el jugador tiene el objetivo necesario (Activo/Bench).

**Ayuda**: [typing.Literal](https://docs.python.org/3/library/typing.html#typing.Literal) · [Funciones de orden superior](https://docs.python.org/3/howto/functional.html)

---

## 19) Supporter (límite 1 por turno)

**Enunciado**: Añade `has_played_supporter: bool` en `Player`. Implementa `play_supporter(player, card)` que aplique un efecto (p.ej., descarta la mano y roba 7) y haga cumplir **1 Supporter por turno**.

**Descripción breve**: Introduces otra **regla global** de turno.

**Objetivos**:

* Validar disponibilidad antes de jugar Supporter.
* Efecto ejemplo: “descarta mano y roba 7”.
* Reset del flag al cambiar de turno.

**Ayuda**: [Gestión de listas (borrar/mover)](https://docs.python.org/3/tutorial/datastructures.html) · [random.sample/draw](https://docs.python.org/3/library/random.html)

---

## 20) Stadium persistente (efecto global)

**Enunciado**: Añade `game.active_stadium: TrainerCard | None`. Al jugar un Stadium, si hay uno activo, se descarta. Aplica su efecto global en el cálculo de daño (p.ej., “+10 daño a ataques de tipo FIRE”).

**Descripción breve**: Incorporas **efectos continuos** que afectan a ambos jugadores.

**Objetivos**:

* Soportar 1 Stadium activo a la vez.
* Integrarlo en `compute_damage` (o pipeline posterior).
* Probar conflicto: sustituir Stadium y verificar descarte del anterior.

**Ayuda**: [Diseño de módulos](https://docs.python.org/3/tutorial/modules.html) · [Buenas prácticas de organización](https://peps.python.org/pep-0008/)

---

### Recomendaciones

* Mantén helpers como `move_card(src, dst, card)` para evitar duplicar lógica.
* Documenta con docstrings (`"""..."""`) cada acción jugable.
* Añade asserts y pruebas rápidas (`pytest` más adelante) para no romper reglas al avanzar.
