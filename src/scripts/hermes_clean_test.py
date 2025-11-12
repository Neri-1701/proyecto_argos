import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))

import pandas as pd
from src.hermes_core import limpiar_catalogo
from pathlib import Path
import datetime

# --- Configuración de rutas ---
data_path = Path(r"C:\Users\felip\Documents\GitHub\proyecto_argos\data\external\CatalogoAnexos.xlsx")
output_path = Path(r"C:\Users\felip\Documents\GitHub\proyecto_argos\data\processed\catalogo_limpio.xlsx")
log_path = Path(r"C:\Users\felip\Documents\GitHub\proyecto_argos\reports\hermes_limpieza.log")

# --- Carga ---
df = pd.read_excel(data_path)
print(f"Tamaño antes: {len(df)}")

# --- Limpieza ---
df_limpio = limpiar_catalogo(df)
print(f"Tamaño después: {len(df_limpio)}")

# --- Guardado ---
output_path.parent.mkdir(parents=True, exist_ok=True)
df_limpio.to_excel(output_path, index=False)

# --- Registro en log ---
log_path.parent.mkdir(parents=True, exist_ok=True)
with open(log_path, "a", encoding="utf-8") as log:
    log.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] "
              f"Limpieza completada. {len(df)} → {len(df_limpio)} registros. Archivo: {output_path}\n")

print(f"\n✅ Limpieza completada y guardada en: {output_path}")
print(f"🧾 Registro actualizado en: {log_path}")
