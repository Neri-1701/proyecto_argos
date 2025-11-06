"""
CLI de ARGOS (Hermes Alpha 0.1.0) usando Typer.

Uso recomendado:
    python -m src.main predict "VALVULA GLOBO ACERO 2 PULG CLASE 600"

Tambien se puede ejecutar como script directo:
    python src/main.py predict "VALVULA GLOBO ACERO 2 PULG CLASE 600"
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from src.models.classify_family import predict_family
from src.models.search_material import search_material
from src.preprocess.preprocess_text import clean_description

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


@app.command()
def predict(descripcion: str):
    """
    Predice la familia y sugiere el mejor codigo por similitud.
    """
    cleaned = clean_description(descripcion)
    family = predict_family(cleaned)
    code, desc, score = search_material(cleaned)

    table = Table(title="ARGOS - Prediccion y Sugerencia", show_lines=False)
    table.add_column("Campo", style="cyan", no_wrap=True)
    table.add_column("Valor", style="white")

    table.add_row("Entrada", descripcion)
    table.add_row("Descripcion limpia", cleaned)
    table.add_row("Familia predicha", family)
    table.add_row("Codigo sugerido", code)
    table.add_row("Descripcion sugerida", desc)
    table.add_row("Score similitud", f"{score:.4f}")

    console.print(table)


if __name__ == "__main__":
    app()

