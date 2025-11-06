"""
Busqueda semantica sencilla por similitud coseno usando TF-IDF.

- Carga el inventario simulado en memoria
- Limpia y vectoriza descripciones
- Devuelve el material mas similar a una consulta dada
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.load_secure_data import load_inventory
from src.preprocess.preprocess_text import clean_description


def search_material(text: str) -> Tuple[str, str, float]:
    """
    Busca el material mas parecido en el inventario simulado.

    Args:
        text: Descripcion libre del usuario

    Returns:
        (COD_MATERIAL, DESCRIPCION_LARGA, score_coseno)
    """
    df = load_inventory()
    if df.empty:
        raise RuntimeError("El inventario simulado esta vacio.")

    inv_texts_clean = [clean_description(t) for t in df["DESCRIPCION_LARGA"].tolist()]
    query_clean = clean_description(text)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, norm="l2")
    X_inv = vectorizer.fit_transform(inv_texts_clean)
    X_q = vectorizer.transform([query_clean])

    sims = cosine_similarity(X_q, X_inv).ravel()
    best_idx = int(np.argmax(sims))
    best_score = float(sims[best_idx])

    best_code = str(df.iloc[best_idx]["COD_MATERIAL"])
    best_desc = str(df.iloc[best_idx]["DESCRIPCION_LARGA"])

    return best_code, best_desc, best_score

