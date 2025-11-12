# ================================================================
# hermes_core/train_familia.py
# Entrenamiento del modelo Hermes-Core (clasificación de familia)
# ================================================================

import pandas as pd
import numpy as np
import joblib
import datetime
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from hermes_core.data_cleaning import limpiar_catalogo

# ------------------------------------------------
# Función principal de entrenamiento
# ------------------------------------------------
def entrenar_modelo_familia(df: pd.DataFrame, modelo_dir="models/hermes/familia/") -> dict:
    """Entrena el modelo Hermes-Core para clasificación de familia."""

    # Limpieza y preparación
    df = limpiar_catalogo(df)
    X = df["Descripcion"].astype(str)
    y = df["FAMILIA"].astype(str)

    # División entrenamiento / prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Generación de embeddings
    print("Cargando modelo de embeddings...")
    embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    print("Generando embeddings de entrenamiento...")
    X_train_emb = embedder.encode(X_train.tolist(), show_progress_bar=True, convert_to_numpy=True)
    print("Generando embeddings de prueba...")
    X_test_emb = embedder.encode(X_test.tolist(), show_progress_bar=True, convert_to_numpy=True)

    # Entrenamiento del modelo
    print("Entrenando modelo de clasificación de FAMILIA...")
    model = LogisticRegression(max_iter=2000, n_jobs=-1)
    model.fit(X_train_emb, y_train)

    # Evaluación
    print("\nEvaluando desempeño del modelo...")
    y_pred = model.predict(X_test_emb)
    reporte = classification_report(y_test, y_pred, digits=3)
    print(reporte)

    # Guardado
    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"{modelo_dir}hermes_model_familia_{fecha}.pkl"
    embed_path = f"{modelo_dir}hermes_embedder_{fecha}.pkl"
    data_path = f"{modelo_dir}hermes_dataset_splits_{fecha}.pkl"

    joblib.dump(model, model_path)
    joblib.dump(embedder, embed_path)
    joblib.dump((X_train_emb, X_test_emb, y_train, y_test), data_path)

    print(f"\nModelos guardados en: {modelo_dir}")

    return {
        "modelo": model_path,
        "embedder": embed_path,
        "dataset": data_path,
        "reporte": reporte,
    }


# ------------------------------------------------
# Ejecución directa
# ------------------------------------------------
if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Entrenamiento Hermes-Core (FAMILIA)")
    parser.add_argument("--input", type=str, required=True, help="Ruta del catálogo limpio (Excel o CSV)")
    parser.add_argument("--output", type=str, default="models/hermes/familia/", help="Carpeta destino para los modelos")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print(f"Leyendo dataset desde: {args.input}")

    if args.input.endswith(".xlsx"):
        df = pd.read_excel(args.input)
    else:
        df = pd.read_csv(args.input)

    entrenar_modelo_familia(df, modelo_dir=args.output)
