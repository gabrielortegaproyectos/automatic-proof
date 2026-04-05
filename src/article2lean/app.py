"""Shared application-level explanations used by the minimal CLI."""

from __future__ import annotations


SYSTEM_OVERVIEW = (
    "article2lean convierte texto matematico informal en un camino estructurado "
    "hacia la formalizacion en Lean."
)

SUBSYSTEM_DESCRIPTIONS = {
    "ingestion": "Lee Markdown o teoremas aislados y normaliza la fuente cruda.",
    "segmentation": "Encuentra bloques matematicos como definiciones, teoremas y pruebas.",
    "references": "Rastrea citas, referencias locales y estructura de dependencias.",
    "sketches": "Construye y refina argument sketches, la capa central de razonamiento.",
    "formalization": "Transforma matematica estructurada en pasos orientados a Lean.",
    "proving": "Ejecuta chequeos Lean y recoge retroalimentacion de verificacion.",
    "orchestrators": "Conecta subsistemas en flujos de articulo y teorema.",
    "exporters": "Emite reportes legibles y artefactos Lean.",
}


def describe_architecture() -> str:
    """Return a concise explanation of the current system map."""

    lines = [SYSTEM_OVERVIEW, "", "Mapa de subsistemas:"]
    for name, description in SUBSYSTEM_DESCRIPTIONS.items():
        lines.append(f"- {name}: {description}")
    return "\n".join(lines)


def describe_article_mode(source_path: str | None = None) -> str:
    """Explain the future role of the article pipeline."""

    suffix = f" Entrada recibida: {source_path}." if source_path else ""
    return (
        "El modo article leera en el futuro un articulo Markdown, segmentara sus "
        "bloques matematicos, construira argument sketches y coordinara pasos de "
        f"formalizacion orientados a Lean.{suffix}"
    )


def describe_theorem_mode(statement: str | None = None) -> str:
    """Explain the future role of the single-theorem pipeline."""

    suffix = f" Enunciado recibido: {statement}." if statement else ""
    return (
        "El modo theorem partira en el futuro desde un teorema aislado, construira "
        "un primer argument sketch y lo refinara hacia obligaciones Lean."
        f"{suffix}"
    )
