# Pokémon TCG – Bloque MID (21–30)

Tercer bloque en **Python** para añadir arquitectura y efectos avanzados al sistema de combate tipo **Pokémon TCG**. Cada ejercicio incluye: **Enunciado**, **Descripción breve**, **Objetivos**, y **Ayuda**.

---

## 21) RNG inyectable (Coin Flip y más)

**Enunciado**: Crea una interfaz de RNG `IRng` (con `Protocol` o `ABC`) con el método `coin_flip() -> bool`. Implementa `DefaultRng` con `random`. Inyecta el RNG en `GameState` para que los sistemas que lo necesiten **no** llamen a `random` directamente.

**Descripción breve**: Desacoplas la aleatoriedad mediante **inyección de dependencias**, facilitando testeo y reproducibilidad (semillas).

**Objetivos**:

* Definir `IRng` con `typing.Protocol` **o** `abc.ABC`.
* Implementar `DefaultRng(seed: int | None)` con `random.Random` interno.
* Añadir `rng` a `GameState` y usarlo en coin flips futuros.

**Ayuda**: [typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) · [abc — Clases abstractas](https://docs.python.org/3/library/abc.html) · [random.Random](https://docs.python.org/3/library/random.html#random.Random)

---

## 22) Estados: Dormido y Paralizado

**Enunciado**: Amplía `Status` con `ASLEEP` y `PARALYZED`. Implementa reglas: Dormido → al final de tu turno tira moneda; si **cara**, despierta. Paralizado → no puede atacar durante tu turno actual.

**Descripción breve**: Añades **estados** que condicionan acciones y se resuelven por fases.

**Objetivos**:

* `Status` enum con `NONE, ASLEEP, PARALYZED`.
* Hook en `Phase.END` para resolver despertar.
* Bloqueo de ataque en `Phase.ATTACK` si `PARALYZED`.

**Ayuda**: [Enum](https://docs.python.org/3/library/enum.html) · (recordatorio) RNG del ejercicio 21.

---

## 23) Pipeline de daño (modificadores encadenados)

**Enunciado**: Crea `DamageContext(attacker, defender, attack, amount_base)` y una interfaz `IDamageModifier` con `modify(ctx) -> None`. Aplica un **orden**: base → debilidad/resistencia → stadium/abilities → clamp `[0, ∞)`. Permite registrar modificadores activos.

**Descripción breve**: Estructuras el cálculo de daño como **middleware** extensible.

**Objetivos**:

* `DamageContext` inmutable salvo `amount_actual`.
* Colección de `IDamageModifier` en `GameState` (o derivada del estado).
* Tests manuales con dos modificadores y verificación de orden.

**Ayuda**: [dataclasses](https://docs.python.org/3/library/dataclasses.html) · [Patrón middleware (artículo)](https://en.wikipedia.org/wiki/Middleware) *(referencia conceptual)*

---

## 24) Abilities pasivas (hooks)

**Enunciado**: Define `Ability` con nombre y hooks opcionales: `on_modify_damage(ctx)`, `on_turn_end(state)`, etc. Permite que un `PokemonCard` tenga 0..n habilidades. Implementa un ejemplo: **Thick Fat** (−20 daño recibido de `FIRE` y `WATER`).

**Descripción breve**: Introduces **comportamientos pasivos** reutilizables por carta.

**Objetivos**:

* Modelo `Ability` con funciones callback opcionales.
* Integración de `on_modify_damage` en el pipeline (ej. 23).
* Demostración con al menos 1 habilidad pasiva.

**Ayuda**: [Callable y `typing` avanzados](https://docs.python.org/3/library/typing.html#typing.Callable)

---

## 25) Efectos con duración (buff/debuff temporales)

**Enunciado**: Implementa `Effect(id, turns_left, on_apply, on_expire)` aplicables a `Pokemon` o `Player`. Al final de cada turno, decrementa `turns_left`; si llega a 0, ejecuta `on_expire` y elimina el efecto.

**Descripción breve**: Gestión de **estado temporal** con ciclo de vida controlado por turnos.

**Objetivos**:

* Contenedor de efectos con destino (`target`: pokemon/jugador).
* Hooks `on_apply/on_expire` y registro en `GameState`.
* Un buff `+10` al daño del Activo durante 2 turnos como ejemplo.

**Ayuda**: [Gestión de listas (eliminar mientras iteras)](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

---

## 26) Pila de acciones (Stack) y respuestas

**Enunciado**: Crea `ActionStack` (LIFO) con operaciones `push`, `pop`, `resolve_all`. Simula secuencia: atacante declara ataque → defensor juega un `Item` de respuesta (p.ej., `Switch`) → resuelve el stack en orden inverso.

**Descripción breve**: Modelo para **reacciones** y orden de resolución.

**Objetivos**:

* Definir una abstracción `Action` o `Command` con `execute(state)`.
* `ActionStack` que resuelva en LIFO.
* Demostración con ataque + respuesta.

**Ayuda**: [Pilas con listas](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks) · [Command pattern](https://refactoring.guru/design-patterns/command)

---

## 27) Costes alternativos (descartar energías específicas)

**Enunciado**: Diseña interfaz `ICost` con `can_pay(pokemon)` y `pay(pokemon)`. Soporta costes del tipo: “descarta 1 energía `FIRE` adjunta” versus “paga 1 `COLORLESS`”. Asocia `ICost` a `Attack`.

**Descripción breve**: Generalizas los **costes** de acciones para soportar reglas especiales.

**Objetivos**:

* Implementar al menos dos `ICost` distintos.
* Integrar en `can_pay_attack`/`pay_attack` sin romper compatibilidad.
* Manejar errores claros cuando no se puede pagar.

**Ayuda**: [Protocol/ABC](https://docs.python.org/3/library/abc.html) · [Excepciones personalizadas](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions)

---

## 28) Estados avanzados: Confused, Poisoned, Burned

**Enunciado**: Amplía `Status` y sus reglas:

* **Confused**: al atacar, tira moneda; si cruz, el atacante recibe 30 de daño y no golpea.
* **Poisoned**: al final de turno, recibe +10.
* **Burned**: al final de turno, recibe +20 y tira moneda para curarse (si cara, quita Burned).

**Descripción breve**: Añades más **mecánicas entre fases** con RNG.

**Objetivos**:

* Integrar estos estados en `Phase.ATTACK` y `Phase.END`.
* Usar el RNG inyectado para las monedas.
* Probar 2 turnos simulados con Poison y Burn.

**Ayuda**: [Organización por fases y hooks](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)

---

## 29) Búsqueda en mazo (search & reveal)

**Enunciado**: Implementa utilidades:

* `search_deck(player, predicate, max_n) -> list[Card]`
* `reveal_and_add_to_hand(player, cards)`
  Crea un Item que busque “1 Pokémon Básico” y lo revele antes de ir a la mano.

**Descripción breve**: Estandarizas la **tutorización** (buscar cartas) con predicados.

**Objetivos**:

* Predicados reutilizables (ej., `is_basic_pokemon`).
* Movimiento de cartas deck → mano con revelado en log/evento.
* Barajar el mazo tras la búsqueda si aplica.

**Ayuda**: [Funciones de orden superior](https://docs.python.org/3/howto/functional.html) · [random.shuffle](https://docs.python.org/3/library/random.html#random.shuffle)

---

## 30) Registro de eventos (Event Bus) y Battle Log

**Enunciado**: Crea un `EventBus` con `publish(event_name, payload)` y `subscribe(event_name, callback)`. Emite eventos clave: `card_played`, `damage_dealt`, `knockout`, `status_applied`. Mantén un `battle_log: list[str]` legible para usuarios.

**Descripción breve**: Separas **notificación** de lógica central y creas trazabilidad.

**Objetivos**:

* Subscripción/desubscripción segura (evitar duplicados o fugas).
* Formatear mensajes de log claros y compactos.
* Ver un turno completo con eventos publicados en orden.

**Ayuda**: [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) · [Logging en Python (módulo `logging`)](https://docs.python.org/3/library/logging.html)

---

### Recomendaciones

* Define errores propios (`GameError`) para fallos de reglas/costes.
* Usa `dataclasses.field(default_factory=...)` para listas/dicts.
* Mantén pruebas rápidas con `assert` o inicia una batería con `pytest` (se formaliza en el bloque Senior).
