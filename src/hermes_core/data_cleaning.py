# ================================================================
# hermes_core/data_cleaning.py
# Módulo de limpieza y normalización del catálogo de materiales
# ================================================================

import pandas as pd
import numpy as np
import re
import unidecode

# ------------------------------------------------
# Limpieza de texto técnico
# ------------------------------------------------
def limpiar_texto(txt: str) -> str:
    """Normaliza un texto técnico sin eliminar unidades o medidas."""
    if pd.isna(txt):
        return "-"
    txt = str(txt).upper()
    txt = unidecode.unidecode(txt)
    txt = re.sub(r'[“”"″´`]', ' ', txt)
    txt = re.sub(r'(\d+)\s*/\s*(\d+)', r'\1/\2', txt)
    txt = re.sub(r'[^A-Z0-9/\-\s\.]', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt


# ------------------------------------------------
# Normalización de columnas clave
# ------------------------------------------------
def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza las columnas críticas del catálogo."""
    for col in ['FAMILIA', 'SUB-FAMILIA', 'CLASE', 'MATERIAL', 'ESPECIFICACION']:
        if col not in df.columns:
            df[col] = "-"
        df[col] = (
            df[col].fillna("-")
            .astype(str)
            .str.upper()
            .str.strip()
            .apply(unidecode.unidecode)
        )
    df["Descripcion"] = df["Descripcion"].apply(limpiar_texto)
    return df


# ------------------------------------------------
# Filtrado básico
# ------------------------------------------------
def filtrar_catalogo(df: pd.DataFrame, min_familia=2) -> pd.DataFrame:
    """Elimina filas sin familia y familias con muy pocos registros."""
    df = df[df["FAMILIA"] != "-"]
    freq = df["FAMILIA"].value_counts()
    df = df[df["FAMILIA"].isin(freq[freq >= min_familia].index)].reset_index(drop=True)
    return df


# ------------------------------------------------
# Pipeline de limpieza
# ------------------------------------------------
def limpiar_catalogo(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo de limpieza para Hermes-Core."""
    df = normalizar_columnas(df)
    df = filtrar_catalogo(df, min_familia=2)
    return df