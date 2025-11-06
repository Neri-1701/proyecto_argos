ARGOS - Sistema Inteligente de Clasificacion y Localizacion de Materiales
Hermes Alpha 0.1.0

Descripcion
- MVP funcional que simula un inventario en memoria.
- Dado un texto libre, limpia y vectoriza, predice familia y sugiere el codigo mas similar por TF-IDF + coseno.

Estructura
- src/utils/text_cleaning.py: Normalizacion y limpieza de texto.
- src/preprocess/preprocess_text.py: clean_description y vectorize_descriptions (TF-IDF).
- src/models/classify_family.py: Clasificador dummy por regex para familia.
- src/models/search_material.py: Busqueda semantica por similitud coseno.
- data/load_secure_data.py: Inventario simulado (pandas DataFrame).
- src/main.py: CLI con Typer.
- tests/test_pipeline.py: Pruebas basicas con pytest.
- dvc.yaml: Stage ficticio de preparacion de datos.

Instalacion
1) Crear y activar entorno (opcional).
2) Instalar dependencias:
   pip install -r requirements.txt

Ejecucion CLI
- Desde la raiz del repo:
  python src/main.py predict "VALVULA GLOBO ACERO 2 PULG CLASE 600"
- Alternativa recomendada:
  python -m src.main predict "VALVULA GLOBO ACERO 2 PULG CLASE 600"

Salida esperada (ejemplo)
- Familia predicha: valvula
- Codigo sugerido: VAL-GLB-AC-2-CL600
- Score similitud: ~1.0

Pruebas
- Ejecutar:
  python -m pytest tests -q

Notas
- Todos los datos estan en memoria; no se requieren archivos externos.
- sentence-transformers esta como placeholder para futuras mejoras.

