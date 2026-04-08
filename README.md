# automatic-proof

`automatic-proof` es el repositorio Git del paquete Python `article2lean`.

La meta de largo plazo del proyecto es tomar texto matematico informal y
convertirlo en un flujo de trabajo que pueda formalizarse progresivamente en
Lean.

## Por que importa esta etapa

Las primeras tareas no intentan formalizar matematicas de punta a punta. Su
trabajo es crear el mapa del sistema y la primera capa de lectura documental
para que las siguientes tareas tengan un lugar claro donde vivir.

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

Este repositorio implementa por ahora el esqueleto del flujo y una primera
ingesta de Markdown.

## Ingesta Markdown actual

La capa `ingestion` ya puede leer un archivo Markdown y convertirlo en un
`MarkdownDocument` con bloques crudos de tipo `heading`, `paragraph` y `list`.

Esta pieza representa la puerta de entrada del modo articulo: todavia no decide
si un bloque es un teorema o una prueba, pero si deja una estructura navegable
que la etapa `segmentation` podra clasificar despues.

```python
from article2lean.ingestion import load_markdown_file

document = load_markdown_file("tests/fixtures/garrido2025inexact.md")
first_block = document.blocks[0]
```

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

## Limitaciones actuales

- La ingesta Markdown actual es simple: solo reconoce headings, parrafos y
  listas planas.
- El proyecto todavia no clasifica bloques matematicos como definiciones,
  teoremas o pruebas.
- El proyecto todavia no construye objetos `ArgumentSketch`.
- El backend de Lean sigue siendo un placeholder.
- La mayoria de los modulos existen para dejar claras las responsabilidades,
  no para ofrecer comportamiento completo todavia.
