# Especificación técnica maestra: sistema unificado de refinamiento matemático a Lean

## 1. Visión general

Este proyecto no debe modelarse como dos aplicaciones separadas:

* una para demostrar teoremas aislados
* otra para formalizar artículos en Markdown

La abstracción central del sistema será el **refinamiento de argumentos matemáticos**. Tanto un teorema aislado como una prueba escrita en un artículo deben convertirse primero a una representación intermedia común llamada `ArgumentSketch`.

El flujo conceptual unificado será:

**entrada matemática informal o parcialmente formal**
→ **segmentación / extracción de estructura**
→ **ArgumentSketch**
→ **refinamiento iterativo de nodos argumentales**
→ **obligaciones formales verificables en Lean**
→ **ensamblado de resultados y reporte**

## 2. Objetivo del sistema

Construir una aplicación Python que pueda:

1. recibir un enunciado matemático aislado y tratar de formalizarlo y/o demostrarlo en Lean
2. recibir un artículo en Markdown con definiciones, teoremas, pruebas, observaciones y referencias
3. segmentar el artículo en bloques matemáticos
4. extraer sketches argumentales desde pruebas parciales o informales
5. refinar esos sketches en pasos más precisos y verificables
6. generar archivos Lean parciales o totales
7. distinguir explícitamente entre:

   * pasos probados
   * pasos asumidos
   * pasos ambiguos
   * huecos de formalización
   * dependencias externas

## 3. Principio de diseño central

El sistema debe operar bajo esta regla:

> Ningún paso matemático queda aceptado como válido solo porque un modelo lo proponga o porque el texto del paper lo sugiera. Un paso queda formalmente aceptado solo si Lean lo verifica o si el sistema lo marca explícitamente como supuesto, axioma, dependencia externa o pendiente.

## 4. Casos de uso principales

### Caso A: teorema aislado

Entrada:

* un enunciado informal, semiformatado o cercano a lenguaje matemático natural

Salida esperada:

* sketch inicial del argumento
* enunciado Lean preliminar
* prueba Lean parcial o total
* reporte de huecos

### Caso B: artículo Markdown

Entrada:

* archivo `.md` con contenido matemático

Salida esperada:

* bloques segmentados
* referencias resueltas o clasificadas
* sketches por resultado o por prueba
* formalización Lean por unidades
* archivo Lean ensamblado
* reporte de cobertura y huecos

## 5. Abstracción central: ArgumentSketch

### 5.1 Motivación

Los papers rara vez contienen pruebas completamente listas para una traducción directa a Lean. Lo que normalmente contienen es una mezcla de:

* ideas globales
* invocaciones a resultados previos
* reducciones de objetivos
* construcciones parciales
* pasos omitidos
* frases de alto nivel como “se sigue por compacidad”, “por semicontinuidad”, “tomando una subsucesión”, “el resto es estándar”

Por lo tanto, el sistema debe operar sobre una representación intermedia que capture **estructura argumental** y no solo texto plano.

### 5.2 Modelo conceptual

`ArgumentSketch` representa una prueba o razonamiento parcial como un grafo o árbol de nodos argumentales.

Cada nodo puede corresponder a:

* objetivo principal
* reducción a subobjetivo
* uso de lema
* aplicación de definición
* construcción de testigo
* contradicción
* partición en casos
* dependencia externa
* paso todavía ambiguo

### 5.3 Modelo de datos sugerido

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ArgumentNode:
    node_id: str
    kind: str
    text: str
    formal_goal: Optional[str] = None
    status: str = "open"  # open | refined | verified | failed | assumed | deferred
    parent_id: Optional[str] = None
    children_ids: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    lean_fragment: Optional[str] = None
    source_block_id: Optional[str] = None
    confidence: float = 0.0
    metadata: dict = field(default_factory=dict)

@dataclass
class ArgumentSketch:
    sketch_id: str
    title: str
    root_node_id: str
    nodes: dict[str, ArgumentNode] = field(default_factory=dict)
    source_type: str = "theorem"  # theorem | article_block
    metadata: dict = field(default_factory=dict)
```

## 6. Tipos de huecos

El sistema debe clasificar huecos explícitamente. No todos los fallos son iguales.

### Tipos de huecos sugeridos

* `formalization_gap`: se entiende la idea matemática, pero no se ha logrado traducirla a Lean
* `logical_gap`: el argumento salta pasos necesarios
* `dependency_gap`: se cita o usa un resultado no disponible todavía
* `semantic_gap`: la formulación textual es demasiado ambigua
* `suspected_false_step`: el paso parece matemáticamente incorrecto o insuficiente

Modelo sugerido:

```python
@dataclass
class ArgumentHole:
    hole_id: str
    node_id: str
    hole_type: str
    description: str
    severity: str = "medium"
    suggested_action: str | None = None
    metadata: dict = field(default_factory=dict)
```

## 7. Arquitectura de alto nivel

El sistema debe dividirse en cuatro subsistemas.

### 7.1 Ingesta documental

Responsable de:

* leer Markdown
* construir AST o estructura equivalente
* normalizar bloques

### 7.2 Segmentación matemática

Responsable de:

* detectar definiciones, teoremas, pruebas, etc.
* enlazar pruebas con enunciados
* detectar referencias

### 7.3 Extracción y refinamiento de sketches

Responsable de:

* construir `ArgumentSketch`
* elegir nodos abiertos
* refinar nodos en subpasos
* clasificar huecos

### 7.4 Verificación Lean

Responsable de:

* traducir enunciados y micro-pasos a Lean
* ejecutar Lean
* devolver errores, metas y evidencia de progreso

## 8. Orquestadores

### 8.1 DocumentIngestionOrchestrator

Objetivo:

* recibir un `.md`
* generar bloques segmentados
* resolver dependencias básicas
* construir sketches iniciales

### 8.2 SketchRefinementEngine

Objetivo:

* tomar un `ArgumentSketch`
* seleccionar un nodo abierto
* decidir si el nodo:

  * puede formalizarse directamente
  * debe subdividirse
  * requiere búsqueda de lema
  * depende de resultado externo
  * debe marcarse como asumido
* actualizar el sketch

### 8.3 LeanVerificationEngine

Objetivo:

* traducir una obligación puntual a Lean
* ejecutar y verificar
* devolver resultado estructurado

### 8.4 ArticleFormalizationOrchestrator

Objetivo:

* coordinar todo el pipeline del artículo
* reunir unidades formales
* ensamblar archivo Lean
* emitir reporte final

## 9. Estructura de carpetas recomendada

```text
article2lean/
├── pyproject.toml
├── README.md
├── configs/
│   ├── app.yaml
│   ├── segmentation.yaml
│   ├── refinement.yaml
│   └── lean.yaml
├── src/article2lean/
│   ├── __init__.py
│   ├── cli.py
│   ├── app.py
│   ├── models/
│   │   ├── article_models.py
│   │   ├── sketch_models.py
│   │   ├── proof_models.py
│   │   └── enums.py
│   ├── ingestion/
│   │   ├── markdown_loader.py
│   │   ├── pandoc_loader.py
│   │   └── ast_normalizer.py
│   ├── segmentation/
│   │   ├── heading_rules.py
│   │   ├── inline_label_rules.py
│   │   ├── proof_linker.py
│   │   └── block_classifier.py
│   ├── references/
│   │   ├── theorem_reference_resolver.py
│   │   ├── citation_resolver.py
│   │   └── dependency_graph.py
│   ├── sketches/
│   │   ├── sketch_extractor.py
│   │   ├── sketch_refiner.py
│   │   ├── hole_classifier.py
│   │   ├── node_selector.py
│   │   └── proof_obligation_generator.py
│   ├── formalization/
│   │   ├── statement_formalizer.py
│   │   ├── proof_step_segmenter.py
│   │   ├── assumption_manager.py
│   │   ├── lean_name_generator.py
│   │   └── lean_assembler.py
│   ├── proving/
│   │   ├── lean_backend.py
│   │   ├── executor.py
│   │   ├── planner.py
│   │   ├── retriever.py
│   │   ├── tactic_agent.py
│   │   ├── critic.py
│   │   └── repair.py
│   ├── orchestrators/
│   │   ├── document_ingestion.py
│   │   ├── sketch_refinement.py
│   │   ├── lean_verification.py
│   │   └── article_formalization.py
│   ├── exporters/
│   │   ├── lean_exporter.py
│   │   ├── report_exporter.py
│   │   └── graph_exporter.py
│   └── utils/
│       ├── text.py
│       ├── ids.py
│       └── regexes.py
└── tests/
```

## 10. Modelos principales adicionales

### 10.1 Bloques del artículo

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ArticleBlock:
    block_id: str
    block_type: str
    raw_text: str
    title: Optional[str] = None
    label: Optional[str] = None
    section_path: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    proof_for: Optional[str] = None
    metadata: dict = field(default_factory=dict)
```

### 10.2 Unidades de formalización

```python
@dataclass
class FormalizationUnit:
    unit_id: str
    source_block_id: str
    kind: str
    informal_text: str
    lean_name: Optional[str] = None
    lean_statement: Optional[str] = None
    lean_proof: Optional[str] = None
    dependencies: list[str] = field(default_factory=list)
    assumed: bool = False
    status: str = "pending"
```

### 10.3 Resultado del artículo

```python
@dataclass
class ArticleFormalizationResult:
    units: list[FormalizationUnit]
    sketches: list[ArgumentSketch]
    assumptions: list[str]
    unresolved_references: list[str]
    generated_lean: str
    holes: list[ArgumentHole] = field(default_factory=list)
```

## 11. Políticas de dependencias faltantes

El sistema debe manejar resultados citados pero no probados localmente.

```python
from enum import Enum

class MissingProofPolicy(str, Enum):
    FAIL = "fail"
    ASSUME_AXIOM = "assume_axiom"
    INSERT_SORRY = "insert_sorry"
    SEARCH_LIBRARY = "search_library"
    DEFER = "defer"
```

### Comportamiento esperado

* `FAIL`: detener el pipeline
* `ASSUME_AXIOM`: generar axioma explícito
* `INSERT_SORRY`: generar stub con `by sorry`
* `SEARCH_LIBRARY`: intentar enlazar con biblioteca existente
* `DEFER`: registrar como pendiente sin bloquear el resto

## 12. Flujo detallado del artículo

1. cargar Markdown
2. extraer bloques crudos
3. clasificar bloques matemáticos
4. enlazar pruebas con enunciados
5. extraer referencias
6. resolver referencias locales
7. construir grafo de dependencias
8. crear `FormalizationUnit` para definiciones y resultados
9. crear `ArgumentSketch` para pruebas o estrategias
10. ejecutar refinamiento iterativo sobre sketches
11. traducir resultados parciales a Lean
12. ensamblar archivo Lean
13. chequear archivo Lean completo
14. generar reporte

## 13. Flujo detallado del teorema aislado

1. recibir enunciado
2. generar unidad formal preliminar
3. crear `ArgumentSketch` inicial con uno o pocos nodos
4. refinar sketch iterativamente
5. verificar cada obligación en Lean
6. producir prueba Lean parcial o total
7. generar reporte de huecos

## 14. Interfaz entre refinamiento y Lean

La comunicación entre el refinador y la capa Lean debe ser estructurada.

### Obligación formal

```python
@dataclass
class ProofObligation:
    obligation_id: str
    node_id: str
    informal_goal: str
    lean_goal: str | None = None
    local_context: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
```

### Resultado de Lean

```python
@dataclass
class LeanCheckResult:
    ok: bool
    code: str
    stdout: str
    stderr: str
    goals_before: list[str] = field(default_factory=list)
    goals_after: list[str] = field(default_factory=list)
    error_message: str | None = None
```

## 15. Responsabilidades por módulo

### `markdown_loader.py`

* leer Markdown
* devolver estructura base

### `heading_rules.py`

* detectar tipos de bloques por encabezados

### `inline_label_rules.py`

* detectar tipos de bloques por etiquetas inline

### `proof_linker.py`

* vincular pruebas con statements

### `theorem_reference_resolver.py`

* extraer y resolver referencias textuales

### `dependency_graph.py`

* construir DAG entre bloques y unidades

### `statement_formalizer.py`

* crear `FormalizationUnit` desde bloques matemáticos

### `sketch_extractor.py`

* crear sketches desde teoremas o pruebas textuales

### `sketch_refiner.py`

* seleccionar nodo abierto y refinarlo

### `hole_classifier.py`

* clasificar huecos

### `proof_obligation_generator.py`

* convertir nodos a obligaciones Lean

### `assumption_manager.py`

* generar axiomas, stubs o registros diferidos

### `lean_assembler.py`

* ensamblar archivo Lean final

### `executor.py`

* ejecutar Lean por backend intercambiable

## 16. Backend Lean

Debe existir una interfaz abstracta para evitar acoplar el sistema desde el inicio a una sola estrategia de ejecución.

```python
from abc import ABC, abstractmethod

class LeanBackend(ABC):
    @abstractmethod
    def check(self, code: str) -> LeanCheckResult:
        raise NotImplementedError
```

Implementaciones iniciales:

* `CliLeanBackend`: usa `lake env lean`
* `LeanDojoBackend`: stub preparado para integración futura

## 17. Principios para el refinamiento de sketches

El refinador debe operar con pasos pequeños y verificables.

### Un nodo puede evolucionar así

* `open` → `refined`
* `refined` → `verified`
* `open` → `assumed`
* `open` → `failed`
* `open` → `deferred`

### Acciones posibles sobre un nodo

* subdividir en subpasos
* invocar lema o dependencia
* traducir directamente a obligación Lean
* marcar como dependencia externa
* marcar como supuesto
* solicitar mayor contexto o reformulación

## 18. Ejemplo mínimo de sketch

Enunciado:

> Si `n > 2` y `n` es par, entonces `n` no es primo.

Sketch inicial sugerido:

* nodo raíz: demostrar que `n` no es primo

  * subnodo 1: derivar que `2 ∣ n` a partir de la paridad
  * subnodo 2: mostrar que `2` es divisor no trivial
  * subnodo 3: concluir contradicción con primalidad

## 19. Reporte final esperado

El sistema debe producir un reporte entendible para humanos.

### Secciones sugeridas del reporte

* resumen del documento procesado
* bloques detectados
* sketches generados
* unidades formalizadas
* pasos verificados
* pasos asumidos
* dependencias externas
* huecos clasificados
* errores Lean más frecuentes
* cobertura estimada

## 20. Restricciones de desarrollo

* Python 3.11+
* type hints obligatorios
* dataclasses para modelos de dominio
* módulos pequeños y con responsabilidades claras
* pruebas unitarias mínimas para cada etapa
* no mezclar lógica documental con lógica Lean
* no usar LLMs directamente dentro de funciones utilitarias puras
* dejar interfaces intercambiables donde luego se conectará el backend real

## 21. Fases de implementación recomendadas

### Fase 1

* esqueleto del proyecto
* parser Markdown
* segmentación por reglas
* modelos base

### Fase 2

* enlace de pruebas
* resolución de referencias
* grafo de dependencias

### Fase 3

* `FormalizationUnit`
* ensamblado Lean placeholder
* backend Lean por CLI

### Fase 4

* `ArgumentSketch`
* `SketchRefinementEngine`
* clasificación de huecos

### Fase 5

* refinamiento iterativo con obligaciones Lean
* mejoras de heurísticas
* exportación de reportes

### Fase 6

* integración futura con backend más avanzado
* retrieval de lemas
* formalización semiautomática más potente

## 22. Instrucción maestra para Codex

Codex debe entender que el objetivo no es solo programar un parser ni solo generar Lean. Debe implementar una arquitectura unificada donde el núcleo sea el refinamiento de argumentos.

### Prompt maestro sugerido

```text
Refactoriza e implementa una aplicación Python llamada `article2lean` cuyo núcleo conceptual sea el refinamiento de argumentos matemáticos hacia obligaciones Lean verificables.

Objetivos:
1. soportar dos entradas:
   - teorema aislado
   - artículo Markdown
2. convertir ambas entradas a una representación común llamada `ArgumentSketch`
3. soportar segmentación matemática, resolución de referencias, clasificación de huecos y ensamblado Lean
4. mantener una arquitectura modular y extensible

Implementa estas capas:
- ingestion
- segmentation
- references
- sketches
- formalization
- proving
- orchestrators
- exporters

Requisitos técnicos:
- Python 3.11+
- type hints
- dataclasses
- tests unitarios básicos
- CLI mínima
- backend Lean intercambiable

Reglas de arquitectura:
- no mezclar parsing documental con verificación Lean
- no acoplar el proyecto a un backend Lean único
- usar `ArgumentSketch` como representación intermedia central
- distinguir explícitamente entre pasos verificados, asumidos, diferidos y fallidos
```

## 23. Tareas iniciales sugeridas para Codex

1. crear estructura de carpetas y `pyproject.toml`
2. implementar modelos base (`ArticleBlock`, `FormalizationUnit`, `ArgumentNode`, `ArgumentSketch`)
3. implementar parser Markdown simple
4. implementar segmentación por reglas
5. implementar `proof_linker`
6. implementar extractor de referencias
7. implementar grafo de dependencias
8. implementar formalizador placeholder
9. implementar `lean_assembler`
10. implementar `CliLeanBackend`
11. implementar `sketch_extractor`
12. implementar `sketch_refiner` mínimo
13. implementar `hole_classifier`
14. crear reporte final

## 24. Criterio de éxito del MVP

El MVP será exitoso si puede:

* procesar un Markdown pequeño con una definición, un lema, un teorema y una prueba
* segmentar correctamente esos bloques
* construir al menos un sketch argumental
* generar un archivo Lean placeholder coherente
* distinguir entre prueba disponible y dependencia asumida
* generar un reporte final con huecos explícitos

## 25. Criterio de éxito de la siguiente versión

La siguiente versión será exitosa si además puede:

* refinar un sketch en micro-obligaciones
* enviar esas obligaciones a Lean
* registrar qué pasos realmente fueron verificados
* producir una formalización parcial trazable y depurable

## 26. Observación final de diseño

La idea central del proyecto no es “traducir un paper” ni “hacer ATP puro”. La idea central es construir una máquina que tome matemáticas humanas en estado incompleto y las convierta, mediante refinamiento estructurado, en una cadena de compromisos formales claramente clasificados.

Ese principio debe guiar todas las decisiones de diseño futuras.

## 27. Estrategia de ramas en GitHub

El desarrollo debe organizarse con una rama principal estable y ramas de trabajo por bloque funcional.

### Rama base

* `main`: rama estable, siempre en estado razonablemente limpio

### Rama de integración del proyecto

* `feature/article2lean-foundation`: rama paraguas donde se integran los primeros componentes del MVP antes de volver a `main`

### Convención de ramas por tarea

Usar nombres como:

* `feat/01-project-scaffold`
* `feat/02-markdown-ingestion`
* `feat/03-math-segmentation`
* `feat/04-proof-linking`
* `feat/05-reference-resolution`
* `feat/06-dependency-graph`
* `feat/07-formalization-units`
* `feat/08-lean-assembly`
* `feat/09-cli-lean-backend`
* `feat/10-sketch-models`
* `feat/11-sketch-extraction`
* `feat/12-sketch-refinement-mvp`
* `feat/13-hole-classification`
* `feat/14-article-orchestrator`
* `feat/15-reporting`

Cada rama debe corresponder a una tarea que produzca una mejora entendible y verificable.

## 28. Cómo deben escribirse las tareas

Cada tarea debe incluir siempre estas secciones:

1. **Objetivo**: qué pieza se construye
2. **Por qué importa**: cómo encaja en la arquitectura
3. **Qué debe implementar Codex**
4. **Qué debes revisar tú**: parte conceptual que te ayudará a entender el sistema
5. **Criterio de terminado**: cuándo la tarea realmente está lista
6. **Archivos esperados**

Esto es importante porque el proyecto no debe quedar como una caja negra.

## 29. Roadmap por tareas entendibles

### Tarea 01 — Esqueleto del proyecto

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

### Tarea 02 — Ingesta de Markdown

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

### Tarea 03 — Segmentación matemática por reglas

**Branch:** `feat/03-math-segmentation`

**Objetivo**
Clasificar bloques como definición, teorema, lema, prueba, observación, ejemplo o desconocido.

**Por qué importa**
Esta tarea transforma un documento general en un documento matemático estructurado.

**Qué debe implementar Codex**

* `heading_rules.py`
* `inline_label_rules.py`
* `block_classifier.py`
* soporte para etiquetas en inglés y español

**Qué debes revisar tú**

* las reglas de detección
* los casos ambiguos
* cómo decide si algo es una prueba o solo un párrafo

**Criterio de terminado**

* un documento simple se clasifica correctamente en tipos de bloques

**Archivos esperados**

* `src/article2lean/segmentation/heading_rules.py`
* `src/article2lean/segmentation/inline_label_rules.py`
* `src/article2lean/segmentation/block_classifier.py`

### Tarea 04 — Enlace entre pruebas y enunciados

**Branch:** `feat/04-proof-linking`

**Objetivo**
Vincular cada bloque de prueba con el lema, teorema o proposición al que pertenece.

**Por qué importa**
Sin esto no se puede saber qué prueba corresponde a qué resultado.

**Qué debe implementar Codex**

* `proof_linker.py`
* reglas para pruebas inmediatamente posteriores
* soporte mínimo para referencias tipo “Proof of Theorem 2.1”
* detección de pruebas huérfanas

**Qué debes revisar tú**

* cómo el sistema decide la relación entre statement y proof
* qué casos quedarían ambiguos

**Criterio de terminado**

* las pruebas quedan asociadas a sus enunciados cuando eso es razonable
* las pruebas huérfanas se reportan

**Archivos esperados**

* `src/article2lean/segmentation/proof_linker.py`

### Tarea 05 — Resolución de referencias

**Branch:** `feat/05-reference-resolution`

**Objetivo**
Detectar referencias en el texto como “Lemma 2.3”, “previous theorem” o “teorema anterior”.

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

### Tarea 13 — Clasificación de huecos

**Branch:** `feat/13-hole-classification`

**Objetivo**
Clasificar huecos argumentales y de formalización.

**Por qué importa**
Hace que el sistema sea intelectualmente útil, no solo ejecutable.

**Qué debe implementar Codex**

* `hole_classifier.py`
* tipos de huecos definidos en esta especificación
* heurísticas simples iniciales

**Qué debes revisar tú**

* la diferencia entre un hueco lógico y uno de formalización
* por qué esa clasificación ayuda a leer los resultados

**Criterio de terminado**

* el sistema puede asignar tipos de huecos a nodos o fallos

**Archivos esperados**

* `src/article2lean/sketches/hole_classifier.py`

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

### Tarea 15 — Reporte final y explicabilidad

**Branch:** `feat/15-reporting`

**Objetivo**
Generar un reporte entendible para ti sobre lo que el sistema hizo.

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

## 30. Estrategia de integración

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

## 31. Pull requests recomendados

Cada branch debería llegar como un PR pequeño con:

* resumen corto
* por qué importa
* archivos tocados
* demo mínima
* tests añadidos
* dudas o limitaciones conocidas

Formato sugerido:

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

## 32. Prompt maestro para pedirle a Codex tickets entendibles

```text
Quiero que implementes este proyecto por tareas pequeñas y entendibles. No construyas todo de una vez.

Reglas:
1. trabaja sobre una sola tarea por branch
2. cada branch debe corresponder a una mejora funcional y comprensible
3. cada tarea debe incluir:
   - objetivo
   - por qué importa
   - archivos creados o modificados
   - tests
   - limitaciones
4. preserva una arquitectura modular
5. usa dataclasses y type hints
6. no ocultes la lógica importante dentro de funciones demasiado grandes
7. deja comentarios y docstrings que me ayuden a entender el sistema

Empieza por la tarea `feat/01-project-scaffold`.
```

## 33. Prompt individual reusable para cada tarea

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

## 34. Recomendación final de trabajo

No conviene pedirle a Codex que programe la app completa de una vez. Conviene usar esta especificación como mapa, y luego avanzar ticket por ticket, revisando que cada branch te deje una pieza del sistema que tú realmente entiendas.

El objetivo no es solo llegar al software final. El objetivo es que al final puedas mirar la arquitectura y decir con claridad:

* cómo entra un paper
* cómo se segmenta
* cómo se convierte en sketch
* cómo se refinan los pasos
* cómo Lean verifica
* y dónde están todavía los huecos.
