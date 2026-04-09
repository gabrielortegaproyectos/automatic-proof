# Roadmap de tareas — article2lean

## Cómo deben escribirse las tareas

Cada tarea debe incluir siempre estas secciones:

1. **Objetivo**: qué pieza se construye
2. **Por qué importa**: cómo encaja en la arquitectura
3. **Qué debe implementar Codex**
4. **Qué debes revisar tú**: parte conceptual que te ayudará a entender el sistema
5. **Criterio de terminado**: cuándo la tarea realmente está lista
6. **Archivos esperados**

Esto es importante porque el proyecto no debe quedar como una caja negra.

---

### Tarea 01 — Esqueleto del proyecto ✅

**Branch:** `feat/01-project-scaffold`

**Objetivo**
Crear la estructura inicial del repositorio, el `pyproject.toml`, la carpeta `src/`, la carpeta `tests/`, una CLI mínima y los módulos vacíos principales.

**Por qué importa**
Esta tarea define el mapa del sistema. Si esta parte queda clara, después será mucho más fácil entender dónde vive cada responsabilidad.

**Qué debe implementar Codex**

* crear la estructura de carpetas definida en esta especificación
* crear `pyproject.toml`
* crear `README.md`
* crear `src/article2lean/cli.py`
* crear paquetes Python con `__init__.py`
* agregar una CLI mínima con comandos placeholder

**Qué debes revisar tú**

* que las carpetas te hagan sentido
* que la separación entre `ingestion`, `segmentation`, `sketches`, `formalization` y `proving` sea clara
* que el README explique con palabras simples qué hace cada parte

**Criterio de terminado**

* el proyecto instala
* la CLI responde
* la estructura de carpetas coincide con la especificación

**Archivos esperados**

* `pyproject.toml`
* `README.md`
* `src/article2lean/cli.py`

---

### Tarea 02 — Ingesta de Markdown ✅

**Branch:** `feat/02-markdown-ingestion`

**Objetivo**
Leer un archivo Markdown y convertirlo a una estructura navegable.

**Por qué importa**
Esta es la puerta de entrada del modo artículo. Sin esto no hay segmentación ni extracción matemática.

**Qué debe implementar Codex**

* `markdown_loader.py`
* carga de `.md`
* extracción de bloques crudos
* tests con ejemplos pequeños

**Qué debes revisar tú**

* cómo un Markdown se vuelve una lista de bloques
* qué información se conserva de cada bloque
* cómo distinguir entre headings, párrafos y listas

**Criterio de terminado**

* dado un `.md`, el sistema devuelve bloques crudos en una estructura legible
* los tests pasan

**Archivos esperados**

* `src/article2lean/ingestion/markdown_loader.py`
* `tests/test_markdown_loader.py`

---

### Tarea 03 — Segmentación matemática por reglas ✅

**Branch:** `feat/03-math-segmentation`

**Objetivo**
Clasificar bloques como definición, teorema, lema, prueba, observación, ejemplo o desconocido.

**Por qué importa**
Esta tarea transforma un documento general en un documento matemático estructurado. Establece dónde *empieza* cada unidad semántica (theorem, proof, definition…), que es la base para el enlace y la delimitación posterior.

**Qué debe implementar Codex**

* `heading_rules.py`
* `inline_label_rules.py`
* `block_classifier.py`
* soporte para etiquetas en inglés, español, francés y portugués
* soporte para abreviaciones (`Def.`, `Thm.`, `Prop.`, `Lem.`, `Cor.`, `Rem.`, `Obs.`, `Conj.`, `Note`)
* fallback fuzzy con `difflib` para variantes tipográficas

**Qué debes revisar tú**

* las reglas de detección
* los casos ambiguos
* cómo decide si algo es una prueba o solo un párrafo

**Criterio de terminado**

* un documento simple se clasifica correctamente en tipos de bloques
* 137 tests pasan

**Archivos esperados**

* `src/article2lean/segmentation/heading_rules.py`
* `src/article2lean/segmentation/inline_label_rules.py`
* `src/article2lean/segmentation/block_classifier.py`
* `src/article2lean/models/enums.py` (`BlockKind`)

---

### Tarea 04 — Enlace entre pruebas y enunciados + delimitación semántica con LLM

**Branch:** `feat/04-proof-linking`

**Objetivo**
Dos subobjetivos complementarios:

1. **Enlace estructural (reglas):** vincular cada bloque `PROOF` con el lema, teorema o proposición al que pertenece usando los índices que dejó Tarea 03.
2. **Delimitación semántica (LLM):** determinar el alcance completo de cada unidad semántica — cuántos párrafos, listas y continuaciones forman parte del mismo teorema o prueba — usando un modelo de lenguaje.

**Por qué importa**
Un teorema o una prueba raramente ocupa un solo bloque. Puede abarcar múltiples párrafos, listas y sub-argumentos. Tarea 03 detecta dónde *empieza* una unidad semántica pero no dónde *termina*. Esta tarea cierra esa brecha combinando:

* **reglas de proximidad** para el enlace proof→statement (rápido, determinista)
* **ventanas de contexto + LLM** para decidir el alcance real de cada unidad (flexible, robusto ante prosa matemática variada)

**Qué debe implementar Codex**

* `proof_linker.py`:
  * reglas para pruebas inmediatamente posteriores al enunciado
  * soporte para referencias explícitas tipo "Proof of Theorem 2.1"
  * detección de pruebas huérfanas
* Módulo de delimitación semántica (puede vivir en `proof_linker.py` o en un archivo separado):
  * construir **ventanas de contexto** a partir de los bloques clasificados: cada ventana va desde el bloque landmark (THEOREM, LEMMA, PROOF, DEFINITION…) hasta el inicio del siguiente landmark
  * enviar esa ventana al LLM con un prompt que le pida decidir si los bloques dentro de la ventana forman parte de la misma unidad semántica
  * el LLM recibe: tipo del landmark inicial, label, y la lista de bloques siguientes hasta el próximo landmark
  * el LLM devuelve: índice del último bloque que pertenece a esa unidad
  * no es necesario pasarle el documento completo — solo la ventana relevante

**Qué debes revisar tú**

* cómo el sistema decide la relación entre statement y proof
* qué casos quedarían ambiguos con solo reglas (prueba separada del enunciado por una lista, prueba con múltiples párrafos, etc.)
* cómo diseñar el prompt para que el LLM devuelva una respuesta estructurada

**Criterio de terminado**

* las pruebas quedan asociadas a sus enunciados cuando eso es razonable
* las pruebas huérfanas se reportan
* cada unidad semántica tiene marcados sus bloques constitutivos (primer y último bloque)

**Archivos esperados**

* `src/article2lean/segmentation/proof_linker.py`
* tests correspondientes

---

### Tarea 05 — Resolución de referencias

**Branch:** `feat/05-reference-resolution`

**Objetivo**
Detectar referencias en el texto como "Lemma 2.3", "previous theorem" o "teorema anterior".

**Por qué importa**
Aquí aparece la lógica interna del artículo: qué depende de qué.

**Qué debe implementar Codex**

* `theorem_reference_resolver.py`
* extracción de referencias textuales
* resolución local básica
* dejar sin resolver las referencias externas

**Qué debes revisar tú**

* cómo se detectan referencias explícitas e implícitas
* qué diferencias hay entre referencia local y externa

**Criterio de terminado**

* el sistema puede extraer una lista razonable de referencias por bloque

**Archivos esperados**

* `src/article2lean/references/theorem_reference_resolver.py`

---

### Tarea 06 — Grafo de dependencias

**Branch:** `feat/06-dependency-graph`

**Objetivo**
Construir un DAG entre resultados y pruebas.

**Por qué importa**
El grafo permite ordenar la formalización y entender la arquitectura lógica del artículo.

**Qué debe implementar Codex**

* `dependency_graph.py`
* nodos y aristas
* orden topológico
* métodos para consultar padres e hijos

**Qué debes revisar tú**

* cómo una prueba depende de un lema anterior
* por qué el orden topológico importa

**Criterio de terminado**

* el sistema puede producir el orden razonable en que conviene procesar los resultados

**Archivos esperados**

* `src/article2lean/references/dependency_graph.py`

---

### Tarea 07 — Unidades de formalización

**Branch:** `feat/07-formalization-units`

**Objetivo**
Crear la representación intermedia de definiciones, lemas y teoremas que luego se convertirá a Lean.

**Por qué importa**
Esta es la primera capa entre el documento humano y la capa formal.

**Qué debe implementar Codex**

* `FormalizationUnit`
* `statement_formalizer.py`
* generación de nombres Lean placeholder

**Qué debes revisar tú**

* cómo una frase matemática se vuelve una unidad formalizable
* cómo se nombran los resultados en Lean

**Criterio de terminado**

* a partir de bloques matemáticos se generan unidades de formalización coherentes

**Archivos esperados**

* `src/article2lean/formalization/statement_formalizer.py`
* `src/article2lean/models/article_models.py`

---

### Tarea 08 — Ensamblador Lean

**Branch:** `feat/08-lean-assembly`

**Objetivo**
Armar un archivo Lean coherente a partir de unidades de formalización.

**Por qué importa**
Permite ver el primer puente tangible entre documento y Lean.

**Qué debe implementar Codex**

* `lean_assembler.py`
* imports
* namespace
* orden entre definiciones, lemas y teoremas

**Qué debes revisar tú**

* la estructura básica de un archivo Lean
* cómo se ensamblan varias piezas en un solo módulo

**Criterio de terminado**

* el sistema produce un archivo `.lean` placeholder legible

**Archivos esperados**

* `src/article2lean/formalization/lean_assembler.py`

---

### Tarea 09 — Backend Lean por CLI

**Branch:** `feat/09-cli-lean-backend`

**Objetivo**
Chequear un archivo Lean usando `lake env lean`.

**Por qué importa**
Da el primer mecanismo real de verificación, aunque todavía básico.

**Qué debe implementar Codex**

* `lean_backend.py`
* `executor.py`
* `CliLeanBackend`
* resultado estructurado de chequeo

**Qué debes revisar tú**

* cómo el sistema ejecuta Lean
* qué significa que Lean acepte o rechace un archivo
* qué información viene en stdout y stderr

**Criterio de terminado**

* el sistema puede verificar un archivo Lean pequeño y devolver un resultado estructurado

**Archivos esperados**

* `src/article2lean/proving/lean_backend.py`
* `src/article2lean/proving/executor.py`

---

### Tarea 10 — Modelos de sketch

**Branch:** `feat/10-sketch-models`

**Objetivo**
Introducir la abstracción central `ArgumentSketch` y `ArgumentNode`.

**Por qué importa**
Aquí se unifican las dos ramas del proyecto.

**Qué debe implementar Codex**

* `sketch_models.py`
* `ArgumentSketch`
* `ArgumentNode`
* `ArgumentHole`

**Qué debes revisar tú**

* cómo una idea de prueba puede representarse como árbol o grafo
* cómo un nodo captura una parte del argumento

**Criterio de terminado**

* existen modelos limpios y documentados para representar sketches y huecos

**Archivos esperados**

* `src/article2lean/models/sketch_models.py`

---

### Tarea 11 — Extracción de sketches

**Branch:** `feat/11-sketch-extraction`

**Objetivo**
Construir sketches iniciales desde un teorema aislado o desde una prueba textual.

**Por qué importa**
Esta tarea hace real la abstracción unificadora.

**Qué debe implementar Codex**

* `sketch_extractor.py`
* sketch desde teorema aislado
* sketch desde proof block

**Qué debes revisar tú**

* cómo el sistema pasa de texto a estructura argumental
* qué tan fiel o grosero es ese primer sketch

**Criterio de terminado**

* el sistema puede producir sketches mínimos pero útiles en ambos casos

**Archivos esperados**

* `src/article2lean/sketches/sketch_extractor.py`

---

### Tarea 12 — Refinamiento mínimo de sketches

**Branch:** `feat/12-sketch-refinement-mvp`

**Objetivo**
Permitir que el sistema seleccione un nodo abierto y lo refine o lo clasifique.

**Por qué importa**
Este es el corazón conceptual del proyecto.

**Qué debe implementar Codex**

* `node_selector.py`
* `sketch_refiner.py`
* reglas mínimas de refinamiento
* actualización de estado de nodos

**Qué debes revisar tú**

* cuándo un paso se subdivide
* cuándo se intenta formalizar directo
* cuándo se marca como dependencia o supuesto

**Criterio de terminado**

* un sketch puede cambiar de estado y ganar subnodos

**Archivos esperados**

* `src/article2lean/sketches/node_selector.py`
* `src/article2lean/sketches/sketch_refiner.py`

---

### Tarea 13 — Clasificación de huecos

**Branch:** `feat/13-hole-classification`

**Objetivo**
Clasificar huecos argumentales y de formalización.

**Por qué importa**
Hace que el sistema sea intelectualmente útil, no solo ejecutable.

**Qué debe implementar Codex**

* `hole_classifier.py`
* tipos de huecos definidos en la especificación técnica
* heurísticas simples iniciales

**Qué debes revisar tú**

* la diferencia entre un hueco lógico y uno de formalización
* por qué esa clasificación ayuda a leer los resultados

**Criterio de terminado**

* el sistema puede asignar tipos de huecos a nodos o fallos

**Archivos esperados**

* `src/article2lean/sketches/hole_classifier.py`

---

### Tarea 14 — Orquestador del artículo

**Branch:** `feat/14-article-orchestrator`

**Objetivo**
Integrar las piezas del modo artículo en un pipeline único.

**Por qué importa**
Aquí aparece por primera vez una aplicación completa de punta a punta.

**Qué debe implementar Codex**

* `document_ingestion.py`
* `article_formalization.py`
* flujo desde Markdown hasta resultado integrado

**Qué debes revisar tú**

* cómo se conectan los módulos
* en qué orden corre cada etapa
* dónde podrías intervenir si algo sale mal

**Criterio de terminado**

* un `.md` pequeño se procesa de punta a punta y produce un resultado integrado

**Archivos esperados**

* `src/article2lean/orchestrators/document_ingestion.py`
* `src/article2lean/orchestrators/article_formalization.py`

---

### Tarea 15 — Reporte final y explicabilidad

**Branch:** `feat/15-reporting`

**Objetivo**
Generar un reporte entendible sobre lo que el sistema hizo.

**Por qué importa**
El sistema debe ser útil también como herramienta de comprensión, no solo de automatización.

**Qué debe implementar Codex**

* `report_exporter.py`
* resumen de bloques
* sketches generados
* pasos verificados
* dependencias asumidas
* huecos detectados

**Qué debes revisar tú**

* si el reporte te ayuda a entender el comportamiento interno del sistema
* si te permite auditar lo que fue asumido y lo que realmente quedó formalizado

**Criterio de terminado**

* el sistema produce un reporte Markdown claro y útil

**Archivos esperados**

* `src/article2lean/exporters/report_exporter.py`

---

## Estrategia de integración

La integración debe hacerse por etapas.

### Etapa 1

Merge de las ramas 01 a 06 en `feature/article2lean-foundation`

Resultado esperado:

* el sistema ya entiende la estructura del artículo
* todavía no formaliza en serio, pero sí segmenta y ordena

### Etapa 2

Merge de las ramas 07 a 09 en `feature/article2lean-foundation`

Resultado esperado:

* el sistema ya puede generar Lean placeholder y chequearlo por CLI

### Etapa 3

Merge de las ramas 10 a 13 en `feature/article2lean-foundation`

Resultado esperado:

* ya existe el núcleo de `ArgumentSketch`
* ya se puede refinar y clasificar huecos

### Etapa 4

Merge de las ramas 14 y 15 en `feature/article2lean-foundation`

Resultado esperado:

* existe una primera app integrada de punta a punta
* existe un reporte entendible para humanos

### Etapa 5

Merge de `feature/article2lean-foundation` a `main`

---

## Formato recomendado para pull requests

Cada branch debería llegar como un PR pequeño con:

* resumen corto
* por qué importa
* archivos tocados
* demo mínima
* tests añadidos
* dudas o limitaciones conocidas

```text
## Qué cambia
Breve descripción.

## Por qué importa
Cómo encaja en la arquitectura.

## Cómo probarlo
Comandos o inputs mínimos.

## Limitaciones
Qué todavía no resuelve.
```

---

## Prompt individual reusable para cada tarea

Conviene reutilizarlo en el chat cada vez que abras una tarea nueva.

```text
Implementa la tarea `<NOMBRE_DE_LA_TAREA>` en una rama separada.

Necesito que esta tarea no solo funcione, sino que además sea pedagógica para mí.

Incluye:
- código limpio
- docstrings claros
- nombres explícitos
- tests pequeños
- una explicación breve en el README o en comentarios sobre cómo encaja esta pieza en el sistema completo

Al terminar, resume:
1. qué implementaste
2. qué parte del sistema representa
3. cómo puedo probarlo
4. qué limitaciones tiene todavía
```
