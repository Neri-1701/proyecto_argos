# src/preprocess/normalize_types.py

import pandas as pd
from pathlib import Path


def normalize_olet_classes(df, column='tipo_material'):
    """
    Normaliza y agrupa las clases equivalentes de OLET
    (WELDOLET, SOCKOLET, THREDOLET, NIPOLET → OLETS).
    """
    df[column] = df[column].astype(str).str.strip().str.upper()
    olet_types = ['WELDOLET', 'SOCKOLET', 'THREDOLET', 'NIPOLET']
    df[column] = df[column].replace(olet_types, 'OLETS')
    return df


def export_top_families(df, column='tipo_material', top_n=15, output_dir='data/processed/familias'):
    """
    Exporta los N tipos de material más frecuentes a archivos .parquet individuales.
    """
    df[column] = df[column].astype(str).str.strip().str.upper()
    top_families = df[column].value_counts().nlargest(top_n).index.tolist()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for tipo in top_families:
        subset = df[df[column] == tipo]
        filename = f"{tipo.replace('/', '_').replace(' ', '_')}.parquet"
        subset.to_parquet(output_path / filename, index=False)
        print(f"{tipo:<15} → {subset.shape[0]:>5} registros exportados")

    return output_path


def generate_family_parquets(file_path, output_dir="data/processed/familias"):
    """
    Flujo completo: carga, normaliza y exporta .parquet por familia.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {file_path}")

    df = pd.read_parquet(path)
    df = normalize_olet_classes(df)
    output_path = export_top_families(df, output_dir=output_dir)

    print(f"Proceso completado. Archivos generados en: {output_path.resolve()}")
    return output_path
