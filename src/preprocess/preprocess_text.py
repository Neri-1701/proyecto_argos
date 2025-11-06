"""
Preprocesamiento de texto para ARGOS.

Funciones expuestas:
- clean_description(text: str) -> str
- vectorize_descriptions(texts: list[str]) -> np.ndarray

Implementacion con scikit-learn usando un Pipeline demostrativo que encapsula
TfidfVectorizer. No persiste modelos; vectoriza ad-hoc listas en memoria.
"""

from __future__ import annotations

from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from src.utils.text_cleaning import basic_clean


def clean_description(text: str) -> str:
    """
    Limpia una descripcion libre con reglas robustas.
    """
    return basic_clean(text)


def vectorize_descriptions(texts: List[str]) -> np.ndarray:
    """
    Vectoriza una lista de descripciones usando TF-IDF (unigramas y bigramas).

    Retorna:
        np.ndarray: matriz densa [n_samples, n_features]
    """
    cleaned = [clean_description(t) for t in texts]

    pipe = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=1,
                    max_df=1.0,
                    norm="l2",
                ),
            ),
        ]
    )

    X = pipe.fit_transform(cleaned)
    return X.toarray()

