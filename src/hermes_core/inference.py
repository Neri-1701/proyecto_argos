# ================================================================
# hermes_core/inference.py
# Inferencia del modelo Hermes-Core (predicción de familia)
# ================================================================

import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from hermes_core.data_cleaning import limpiar_texto


class HermesPredictor:
    """Cargador y predictor del modelo Hermes-Core."""

    def __init__(self, model_path: str, embedder_path: str):
        """Inicializa el predictor con los modelos entrenados."""
        print("Cargando modelo Hermes-Core...")
        self.model = joblib.load(model_path)
        print("Cargando modelo de embeddings...")
        self.embedder = joblib.load(embedder_path)
        print("Hermes listo para inferencia.")

    def predict_familia(self, descripcion: str):
        """Predice la familia más probable para una descripción dada."""
        texto = limpiar_texto(descripcion)
        emb = self.embedder.encode([texto], convert_to_numpy=True)
        pred = self.model.predict(emb)[0]
        prob = self.model.predict_proba(emb).max()
        return pred, prob


# ------------------------------------------------
# Uso directo desde consola o script
# ------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Inferencia Hermes-Core")
    parser.add_argument("--model", type=str, required=True, help="Ruta al modelo .pkl")
    parser.add_argument("--embedder", type=str, required=True, help="Ruta al embedder .pkl")
    parser.add_argument("--texto", type=str, required=True, help="Descripción a analizar")
    args = parser.parse_args()

    predictor = HermesPredictor(args.model, args.embedder)
    familia, confianza = predictor.predict_familia(args.texto)

    print("\n--------------------------------------------")
    print(f"Descripción: {args.texto}")
    print(f"Familia predicha: {familia}  (confianza: {confianza:.2f})")
    print("--------------------------------------------")
