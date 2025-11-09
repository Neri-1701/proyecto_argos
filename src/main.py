# src/main.py
import sys, os
from src.preprocess.normalize_types import generate_family_parquets
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Agregamos al python path el directorio padre

def main():
    # Definir la base a usar
    database_path = "data/external/MaestroMiscelaneos.parquet"

    # Ejecutar flujo de normalización y exportación
    generate_family_parquets(file_path=database_path)

if __name__ == "__main__":
    main()

