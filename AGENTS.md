# Instrucciones persistentes para Codex

Estas reglas describen como trabajar en este repositorio. Aplican a cualquier
tarea concreta que se pida despues en el chat.

## Flujo de trabajo

1. Trabaja sobre una sola tarea por branch.
2. Cada branch debe corresponder a una mejora funcional y comprensible.
3. No construyas todo el sistema de una vez. Avanza por tareas pequenas.

## Que debe incluir cada tarea

Cada entrega debe dejar claro:

- objetivo
- por que importa
- archivos creados o modificados
- tests
- limitaciones

## Criterios de implementacion

- Preserva una arquitectura modular.
- Usa `dataclasses` y `type hints` cuando aplique.
- No ocultes la logica importante dentro de funciones demasiado grandes.
- Deja comentarios y docstrings que ayuden a entender el sistema.

## Primera tarea sugerida

Empieza por la tarea `feat/01-project-scaffold`.
