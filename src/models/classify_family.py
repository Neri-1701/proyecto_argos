"""
Clasificador jerarquico (dummy) para predecir la familia del material.

Estrategia:
- Limpia el texto
- Busca patrones por regex/keywords
- Devuelve la familia detectada o 'desconocido'
"""

from __future__ import annotations

import re

from src.preprocess.preprocess_text import clean_description


_PATTERNS = [
    ("valvula", re.compile(r"\bvalv|valvula|globo|bola|compuerta\b")),
    ("empaque", re.compile(r"\bempaq|ptfe|gasket|grafit\b")),
    ("esparrago", re.compile(r"\besparr|esp-|esp\b|\bunc\b")),
    ("brida", re.compile(r"\bbrida|flange\b")),
    ("junta", re.compile(r"\bjunta|rtj|anillo\b")),
]


def predict_family(text: str) -> str:
    """
    Predice la familia general de un material a partir de su descripcion.

    Args:
        text: Descripcion libre

    Returns:
        Familia estimada: 'valvula', 'empaque', 'esparrago', 'brida', 'junta' o 'desconocido'
    """
    t = clean_description(text)
    for family, pattern in _PATTERNS:
        if pattern.search(t):
            return family
    return "desconocido"

