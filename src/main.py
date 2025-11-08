from src.pipeline.split_families import split_main
from src.models.classify_family import predict_family
from src.pipeline.predict_pipeline import predict_material

if __name__ == "__main__":
    # Paso 1: separación por familia (si aplica)
    split_main()

    # Paso 2: predicción jerárquica (demo)
    descripcion = "VALVULA GLOBO ACERO 2 PULG CLASE 600"
    familia = predict_family(descripcion)
    result = predict_material(descripcion, familia)
    print(result)
