# src/preprocess/split_families.py

import pandas as pd
from src.preprocess.normalize_types import normalize_olet_classes


def split_families(df, column='tipo_material'):
    """
    Divide el DataFrame por familia de material y devuelve un diccionario
    {familia: subset}.
    """
    # Normaliza primero las familias equivalentes (ej. OLET)
    df = normalize_olet_classes(df, column=column)

    # Agrupa por tipo de material
    families = {fam: subset for fam, subset in df.groupby(column)}

    print(f"Total de familias detectadas: {len(families)}")
    return families
