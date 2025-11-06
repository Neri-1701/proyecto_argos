import pandas as pd
from pathlib import Path

def load_local_parquet(filename="MaestroMiscelaneos.parquet"):
    """
    Carga el dataset localmente desde data/external/
    No intenta acceder a Drive ni a ningún servicio externo.
    """
    file_path = Path(__file__).resolve().parents[2] / "data" / "external" / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo en {file_path}\n"
            "Asegúrate de colocarlo manualmente en data/external/"
        )

    df = pd.read_parquet(file_path)
    print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas.")
    return df

if __name__ == "__main__":
    df = load_local_parquet()
    print(df.head(3))
