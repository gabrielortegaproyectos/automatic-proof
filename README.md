# automatic-proof

`automatic-proof` es el repositorio Git del paquete Python `article2lean`.

La meta de largo plazo del proyecto es tomar texto matematico informal y
convertirlo en un flujo de trabajo que pueda formalizarse progresivamente en
Lean.

## Por que importa esta primera tarea

Esta tarea todavia no intenta formalizar matematicas. Su trabajo es crear el
mapa del sistema para que las siguientes tareas tengan un lugar claro donde
vivir.

Si este esqueleto es facil de leer, entonces el resto del proyecto sera mas
facil de entender, extender y depurar.

## Como encaja esta pieza en el sistema completo

El sistema completo esta pensado asi:

1. Leer una fuente informal, como un teorema aislado o un articulo Markdown.
2. Detectar la estructura matematica dentro de esa fuente.
3. Construir una representacion intermedia del argumento.
4. Refinar ese argumento en obligaciones formales mas pequenas.
5. Enviar esas obligaciones a Lean y recoger los resultados.
6. Exportar un reporte legible de lo probado, asumido o diferido.

Este repositorio implementa por ahora solo el esqueleto de ese flujo.

## Subsistemas

- `ingestion`: lee documentos fuente y los convierte en entradas internas crudas.
- `segmentation`: identifica bloques matematicos como definiciones o pruebas.
- `references`: resuelve referencias textuales y dependencias entre resultados.
- `sketches`: construye y refina argument sketches, la abstraccion central.
- `formalization`: transforma matematica estructurada en artefactos orientados a Lean.
- `proving`: comunica el sistema con Lean o con futuros backends de prueba.
- `orchestrators`: conecta varios subsistemas en flujos completos.
- `exporters`: escribe resultados como archivos Lean, reportes o grafos.
- `models`: guarda los objetos de dominio compartidos por el sistema.
- `utils`: contiene helpers pequenos y reutilizables.

## Inicio rapido

```bash
uv sync
uv run article2lean --help
uv run article2lean architecture
uv run pytest
```

## CLI actual

La CLI es intencionalmente minima y pedagogica por ahora.

- `article2lean article`: placeholder del pipeline futuro para articulos.
- `article2lean theorem`: placeholder del pipeline futuro para teoremas aislados.
- `article2lean architecture`: imprime una explicacion corta del mapa del sistema.

## Como leer los tests

Los tests de esta primera tarea no intentan verificar matematica ni integracion
con Lean. Su objetivo es confirmar que el esqueleto del proyecto quedo
instalado, navegable y entendible.

- `tests/test_cli.py`: prueba la interfaz minima. Verifica que `--help` existe y
  que los comandos placeholder explican su papel dentro del sistema.
- `tests/test_imports.py`: prueba que el paquete y algunos modulos clave se
  puedan importar. Esto sirve para detectar errores tempranos de estructura o de
  empaquetado.
- `tests/test_package_layout.py`: prueba que existan archivos y carpetas que la
  especificacion de la Tarea 01 espera. Es una forma simple de vigilar que el
  scaffold siga alineado con el diseño.

En otras palabras:

1. `test_cli.py` responde a "la puerta de entrada funciona?"
2. `test_imports.py` responde a "el paquete esta bien armado?"
3. `test_package_layout.py` responde a "la estructura coincide con el mapa?"

## Limitaciones actuales

- El proyecto todavia no parsea Markdown.
- El proyecto todavia no construye objetos `ArgumentSketch`.
- El backend de Lean sigue siendo un placeholder.
- La mayoria de los modulos existen para dejar claras las responsabilidades,
  no para ofrecer comportamiento completo todavia.
