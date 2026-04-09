# automatic-proof

`automatic-proof` es el repositorio Git del paquete Python `article2lean`.

La meta de largo plazo del proyecto es tomar texto matematico informal y
convertirlo en un flujo de trabajo que pueda formalizarse progresivamente en
Lean.

## Como encaja esta pieza en el sistema completo

El sistema completo esta pensado asi:

1. Leer una fuente informal, como un teorema aislado o un articulo Markdown.
2. Detectar la estructura matematica dentro de esa fuente.
3. Construir una representacion intermedia del argumento.
4. Refinar ese argumento en obligaciones formales mas pequenas.
5. Enviar esas obligaciones a Lean y recoger los resultados.
6. Exportar un reporte legible de lo probado, asumido o diferido.

## Estado actual del proyecto

| Tarea | Estado | Descripcion |
|-------|--------|-------------|
| 01 — Esqueleto del proyecto | ✅ completa | estructura de carpetas, `pyproject.toml`, CLI minima |
| 02 — Ingesta de Markdown | ✅ completa | `MarkdownDocument` con bloques crudos de heading, paragraph y list |
| 03 — Segmentacion matematica por reglas | ✅ completa | clasificacion de bloques con `BlockKind`, matching con regex + fuzzy + normalizacion multilingue |
| 04 — Enlace pruebas/enunciados + delimitacion semantica con LLM | 🔲 pendiente | `proof_linker.py` + ventanas de contexto para LLM |
| 05 — Resolucion de referencias | 🔲 pendiente | |
| 06 — Grafo de dependencias | 🔲 pendiente | |
| 07 — Unidades de formalizacion | 🔲 pendiente | |
| 08 — Ensamblador Lean | 🔲 pendiente | |
| 09 — Backend Lean por CLI | 🔲 pendiente | |
| 10–15 | 🔲 pendiente | sketches, refinamiento, orquestador, reporte |

El detalle completo de cada tarea esta en [`docs/todo.md`](docs/todo.md).

## Ingesta Markdown

La capa `ingestion` lee un archivo Markdown y lo convierte en un
`MarkdownDocument` con bloques crudos de tipo `heading`, `paragraph` y `list`.

```python
from article2lean.ingestion import load_markdown_file

document = load_markdown_file("tests/fixtures/garrido2025inexact.md")
first_block = document.blocks[0]
```

## Segmentacion matematica

La capa `segmentation` anota cada `ArticleBlock` con un `BlockKind` que
identifica su rol matematico: `THEOREM`, `LEMMA`, `PROOF`, `DEFINITION`,
`PROPOSITION`, `COROLLARY`, `REMARK`, `EXAMPLE`, `OBSERVATION`, `CONJECTURE`,
`NOTATION`, `HEADING`, `PARAGRAPH`, `LIST` o `UNKNOWN`.

La clasificacion opera en dos pasos:

1. **Headings**: `classify_heading(title)` detecta el keyword matematico en el
   titulo del encabezado via regex (path rapido) y fallback fuzzy (path lento).
2. **Parrafos inline**: `classify_inline(text)` detecta etiquetas al inicio del
   parrafo, incluyendo marcadores en negrita/italica.

Ambas capas soportan:

- nombres completos en ingles, espanol, frances y portugues
- abreviaciones (`Def.`, `Thm.`, `Prop.`, `Lem.`, `Cor.`, `Rem.`, `Obs.`, `Conj.`, `Note`)
- variantes tipograficas via `difflib`

```python
from article2lean.segmentation.block_classifier import classify_blocks
from article2lean.ingestion import load_markdown_file

document = load_markdown_file("tests/fixtures/garrido2025inexact.md")
blocks = classify_blocks(document)
theorems = [b for b in blocks if b.block_type == "theorem"]
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

- La segmentacion detecta donde *empieza* cada unidad semantica pero no donde
  *termina*. La delimitacion completa (un teorema puede abarcar varios parrafos
  y listas) se resolvera en Tarea 04 usando un LLM con ventanas de contexto.
- El proyecto todavia no construye objetos `ArgumentSketch`.
- El backend de Lean sigue siendo un placeholder.
- La mayoria de los modulos existen para dejar claras las responsabilidades,
  no para ofrecer comportamiento completo todavia.
