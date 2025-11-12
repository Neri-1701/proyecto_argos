# ================================================================
# hermes_core/utils.py
# Utilidades generales para Hermes-Core / Proyecto ARGOS
# ================================================================

import os
import datetime


# ------------------------------------------------
# Directorios y rutas
# ------------------------------------------------
def ensure_dir(path: str) -> str:
    """Crea un directorio si no existe y devuelve la ruta."""
    os.makedirs(path, exist_ok=True)
    return path


def get_timestamp() -> str:
    """Devuelve un timestamp único (YYYYMMDD_HHMMSS)."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ------------------------------------------------
# Validaciones
# ------------------------------------------------
def validar_archivo(ruta: str):
    """Verifica que un archivo exista antes de usarlo."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    return ruta


def validar_dataframe(df):
    """Verifica que el dataframe no esté vacío."""
    if df is None or len(df) == 0:
        raise ValueError("El DataFrame está vacío o no se cargó correctamente.")
    return df


# ------------------------------------------------
# Logging simple
# ------------------------------------------------
def log(msg: str):
    """Salida estandarizada para logs del sistema ARGOS."""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")
