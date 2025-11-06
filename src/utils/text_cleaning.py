"""
Funciones utilitarias de limpieza y normalizacion de texto para ARGOS.

- Eliminacion de acentos
- Lowercase
- Normalizacion de unidades comunes (pulgadas -> pulg, cl -> clase)
- Eliminacion de puntuacion irrelevante
- Colapsar espacios
"""

from __future__ import annotations

import re
import unicodedata


_WHITESPACE_RE = re.compile(r"\s+")
_NON_ALNUM_KEEP_SOME = re.compile(r"[^a-z0-9/\-\s]")
_DOUBLE_SPACE = re.compile(r"\s{2,}")


def _strip_accents(text: str) -> str:
    text_nfkd = unicodedata.normalize("NFKD", text)
    return "".join([c for c in text_nfkd if not unicodedata.combining(c)])


def _normalize_units(text: str) -> str:
    # Normalizar variaciones comunes en espanol tecnico
    t = text

    # pulgadas -> pulg
    t = re.sub(r"\bpulgadas?\b", "pulg", t)
    t = t.replace('"', " pulg ")

    # clase -> clase N (normalizacion de abreviatura 'cl')
    t = re.sub(r"\bcl\s*(\d+)\b", r"clase \1", t)

    # pulgada singular a 'pulg'
    t = re.sub(r"\bpulgada\b", "pulg", t)

    # Separar medidas mezcladas con letras (p.ej. 2pulg)
    t = re.sub(r"(\d)(pulg)\b", r"\1 \2", t)

    # Espacios alrededor de separadores fraccionales
    t = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1/\2", t)

    return t


def basic_clean(text: str) -> str:
    """
    Limpieza basica y robusta de descripciones tecnicas.
    """
    if not isinstance(text, str):
        text = str(text)

    t = text.strip().lower()

    # Acentos
    t = _strip_accents(t)

    # Normalizacion de unidades
    t = _normalize_units(t)

    # Eliminar caracteres no alfanumericos excepto separadores utiles
    t = _NON_ALNUM_KEEP_SOME.sub(" ", t)

    # Colapsar espacios
    t = _WHITESPACE_RE.sub(" ", t).strip()

    # Reduccion de espacios multiples
    t = _DOUBLE_SPACE.sub(" ", t)

    return t

