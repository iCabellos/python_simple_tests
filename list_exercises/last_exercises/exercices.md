# Pokémon TCG – Bloque SENIOR (31–40)

Cuarto bloque en **Python** para culminar un sistema de combate estilo **Pokémon TCG** con arquitectura sólida, testeo y reproducibilidad. Cada ejercicio incluye: **Enunciado**, **Descripción breve**, **Objetivos**, y **Ayuda**.

---

## 31) Motor de reglas (RuleEngine) y validación previa

**Enunciado**: Implementa una interfaz `IRule` con `validate(action, state) -> list[str]` para retornar mensajes de error. Crea un `RuleEngine` que, dado un `Action`, ejecute todas las reglas y lance un `GameError` si hay violaciones.

**Descripción breve**: Centralizas la **validación de reglas** antes de ejecutar acciones (p. ej., 1 energía/turno, 1 supporter/turno, banco ≤ 5, fase correcta).

**Objetivos**:

* Definir reglas: energía/turno, supporter/turno, tamaño del banco, fase.
* `RuleEngine.assert_valid(action, state)` que acumule y reporte errores.
* Integrar `RuleEngine` en el flujo de juego (previo a `Action.execute`).

**Ayuda**: [abc.ABC](https://docs.python.org/3/library/abc.html) · [Excepciones personalizadas](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions)

---

## 32) Comandos con undo (Command Pattern)

**Enunciado**: Crea una jerarquía `Command` con métodos `do(state)` y `undo(state)`. Implementa comandos: `PlayCard`, `AttachEnergy`, `AttackCommand`, `RetreatCommand`. Mantén un historial para permitir **deshacer** la última acción.

**Descripción breve**: Estandarizas **acciones reversibles** para depurar y ofrecer herramientas de desarrollo.

**Objetivos**:

* Implementar `Command` base y 3–4 comandos concretos.
* Pila de historial (`history`) para `undo`.
* Asegurar que `undo` revierte por completo (mano↔mesa, energía gastada, daño).

**Ayuda**: [Command pattern](https://refactoring.guru/design-patterns/command) · [copy/deepcopy](https://docs.python.org/3/library/copy.html)

---

## 33) DSL declarativo de efectos para Trainer/Abilities

**Enunciado**: Define un **mini DSL** basado en `dict` para describir efectos y un `EffectRunner` que los ejecute. Ejemplos:

```json
{"type":"heal", "who":"active_self", "amount":20}
{"type":"draw", "player":"self", "amount":2}
{"type":"search", "player":"self", "filter":"pokemon_basic", "amount":1}
```

**Descripción breve**: Desacoplas datos (efectos) de lógica (intérprete) para crear cartas **configurables**.

**Objetivos**:

* Diseñar un esquema mínimo y validarlo.
* Implementar handlers para 3–5 tipos de efecto.
* Integrar el DSL en `TrainerCard` y `Ability`.

**Ayuda**: [json](https://docs.python.org/3/library/json.html) · [pydantic (opcional)](https://docs.pydantic.dev/latest/) · [typing.TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)

---

## 34) IA básica de turno (heurística simple)

**Enunciado**: Implementa una IA que, en su `turn()`: (1) adjunte 1 energía si puede al Activo; (2) juegue un Supporter de robo si `len(hand)<4`; (3) seleccione el **mejor ataque** por daño esperado (`expected_damage`), considerando probabilidades de coin flips.

**Descripción breve**: Creas un oponente básico para pruebas y partidas automáticas.

**Objetivos**:

* Función `expected_damage(attack, state)` evaluando coin flips con p=0.5.
* Política simple para jugar cartas.
* Simular IA vs IA durante 10 turnos con log.

**Ayuda**: [random.Random](https://docs.python.org/3/library/random.html) · [itertools](https://docs.python.org/3/library/itertools.html)

---

## 35) Persistencia y carga de partida (save/load)

**Enunciado**: Serializa `GameState` a JSON (ids de cartas, zonas, estados, energías, efectos, prizes, manos, pila, fase, jugador activo). Implementa `from_json` para reconstruir y continuar una partida.

**Descripción breve**: Permites **guardar y reanudar** partidas.

**Objetivos**:

* Métodos `to_json()` / `from_json(data)`.
* Resolver referencias (p. ej., `active` ↔ objetos reales en memoria).
* Tests con una partida guardada y reanudada correctamente.

**Ayuda**: [json](https://docs.python.org/3/library/json.html) · [dataclasses.asdict](https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict)

---

## 36) Validaciones robustas y GameError enriquecido

**Enunciado**: Crea una excepción `GameError` con `code: str`, `message: str`, `context: dict`. Reemplaza errores genéricos por `GameError` en reglas, costes y fases. Añade helpers para formatear mensajes para UI/logs.

**Descripción breve**: Estandarizas **errores claros** y depurables.

**Objetivos**:

* Definir `GameError` y usarlo en todo el flujo.
* Convenios de `code` (ej.: `RULE_ENERGY_ONCE`, `PHASE_INVALID`).
* Tests unitarios que verifiquen códigos y contexto.

**Ayuda**: [Excepciones personalizadas](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions) · [traceback](https://docs.python.org/3/library/traceback.html)

---

## 37) Hooks between-turns y orden de resolución

**Enunciado**: Añade un hook `on_between_turns(state)` que se ejecute entre `END` del jugador actual y `START` del oponente. Usa este hook para Poison/Burn y para algún Stadium/Ability de mantenimiento.

**Descripción breve**: Ajustas el **timing** fino de efectos que se resuelven entre turnos.

**Objetivos**:

* Implementar el hook y llamarlo en el cambio de turno.
* Mover Poison/Burn a este momento si cuadra con tu diseño.
* Testear el **orden**: fin de A → efectos between-turns → inicio de B.

**Ayuda**: [Orden y secuencia en sistemas de eventos](https://docs.python.org/3/library/collections.html#collections.deque)

---

## 38) Attachments enriquecidos (Special Energy & co.)

**Enunciado**: Generaliza energías a un modelo `Attachment` con hooks `on_attach`, `on_detach`, `on_modify_damage`. Implementa **Special Energy** que aporte Colorless y `+10` daño a ataques, y otra que reduzca daño recibido `-10`.

**Descripción breve**: Permites ítems/energías con **efectos pasivos** y ciclo de vida.

**Objetivos**:

* Modelo común `Attachment` y su almacenamiento en `PokemonCard`.
* Invocar hooks al adjuntar/quitar.
* Integración con el pipeline de daño.

**Ayuda**: [Protocol/Callable](https://docs.python.org/3/library/typing.html#typing.Protocol) · [Context Managers (inspiración de hooks)](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers)

---

## 39) Batería de tests con pytest

**Enunciado**: Crea tests que cubran: (a) daño con debilidad/resistencia/stadium/ability, (b) costes alternativos, (c) estados Confused/Poisoned/Burned, (d) evolución preservando daño/energías, (e) regla de 1 supporter por turno.

**Descripción breve**: Formalizas la **calidad** del sistema con pruebas automatizadas.

**Objetivos**:

* 12–20 tests con `pytest` y `fixtures` para mazos sencillos.
* Mock de RNG (semilla fija o `FakeRng`).
* Ejecutar y dejar todo en verde.

**Ayuda**: [pytest – Getting Started](https://docs.pytest.org/en/latest/getting-started.html) · [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

## 40) Partida completa reproducible (demo)

**Enunciado**: Crea `demo_match.py` que juegue una partida corta (IA vs IA) con **semilla fija** del RNG y barajas determinísticas. Imprime un `battle_log` consistente y un **resumen final** (K.O., premios, ganador).

**Descripción breve**: Entregas una **demo end-to-end** estable y verificable.

**Objetivos**:

* Semilla fija para RNG y orden de mazos.
* Log legible con marcas de turno/fase/eventos.
* Resumen con ganador, premios restantes y estado de la mesa.

**Ayuda**: [random.seed](https://docs.python.org/3/library/random.html#random.seed) · [logging](https://docs.python.org/3/library/logging.html)

---

### Sugerencias finales

* Mantén módulos separados (`rules.py`, `commands.py`, `effects.py`, `attachments.py`, `engine.py`).
* Documenta con docstrings y type hints (`mypy` opcional).
* Automatiza `pytest -q` en un script `make test` o `tox` (opcional).
