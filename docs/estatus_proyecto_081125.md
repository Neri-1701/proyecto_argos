# ARGOS – Sistema Inteligente de Clasificación y Localización de Materiales  
## Plan de próximos pasos (etapa de pausa técnica)

---

### 1️.- Consolidar avances actuales

- Se completó la **modularización del pipeline**:
  - `normalize_types.py` → Normalización y separación de familias.
  - `split_families.py` → Agrupación lógica por tipo de material.
  - `main.py` → Punto de entrada del flujo completo.
- Se creó y probó con éxito el **notebook de limpieza de válvulas**, que servirá como plantilla para otras familias.

---

### 2️.- Objetivos inmediatos al reanudar

**A. Formalizar conocimiento experto (fase humana)**
- Documentar cómo un ingeniero reconoce cada familia de material.
- Convertir ese conocimiento en reglas de identificación (`rules.json`):
  - Inclusiones (palabras clave o tokens indicativos)
  - Exclusiones (términos que rompen la coincidencia)
- Ejemplo:
  ```json
  {
    "VALVULA": {
      "inclusion": ["VALV", "VALVE", "BALL", "GLOBE", "BUTTERFLY", "ESF"],
      "exclusion": ["ESPARRAGO", "NIPLE"]
    }
  }
  ```

**B. Crear el módulo `rules_valvulas.py`**
- Contendrá todas las heurísticas expertas que definan qué hace que una descripción sea una válvula.
- Base para validar la eficacia de las reglas contra los datasets curados.

---

### 3️.- Fase semántica – uso de modelos de lenguaje

**Objetivo:** reducir el trabajo manual de rule-mining.

- Usar embeddings preentrenados (ej. `sentence-transformers/LaBSE`, `MiniLM`, o `BETO`) para agrupar descripciones similares.
- Pipeline de inferencia:
  1. Aplicar reglas → resultados claros.
  2. En casos ambiguos → cálculo de similitud semántica con embeddings.
  3. Umbral de similitud (`score > 0.65`) → familia probable.

Ejemplo (pseudo-código):
```python
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/LaBSE')
query = "VALVULA"
emb_query = model.encode(query, convert_to_tensor=True)
emb_desc = model.encode(df["Descripción Larga"].tolist(), convert_to_tensor=True)
scores = util.cos_sim(emb_query, emb_desc)
df["score_valvula"] = scores.squeeze().numpy()
```

---

### 4️.- Fase de aprendizaje (entrenamiento supervisado)

- Entrenar un modelo compacto (`DistilBERT`, `LogisticRegression`, etc.) para reproducir las etiquetas generadas por las reglas y el modelo semántico.
- Dataset de entrenamiento: combinación de materiales curados manualmente + predicciones validadas.
- Guardar el modelo en `models/family_classifier_valvulas.pkl`.

---

### 5️.- Fase MVP (integración total)

- Integrar todas las fases en el flujo:
  1. **Preprocesamiento:** `normalize_types.py`
  2. **Clasificación por familia:** `classify_family.py`
  3. **Limpieza individual:** `clean_pipeline.py`
  4. **Entrenamiento y búsqueda:** `train_pipeline.py`, `search_material.py`

- Flujo jerárquico:
  ```
  Input descripción → Normalización → Reglas → Embeddings → Modelo entrenado → Código sugerido
  ```

---

### 6️.- Fase documental

- Registrar todo el proceso en los notebooks:
  - `00_overview_pipeline.ipynb` → Diagrama general del flujo.
  - `01_rule_design.ipynb` → Definición de heurísticas por familia.
  - `02_clean_valvulas.ipynb` → Limpieza y extracción de atributos.
  - `03_semantic_matching.ipynb` → Pruebas con embeddings.
  - `04_training.ipynb` → Entrenamiento del modelo de clasificación.
- Dejar los notebooks listos para ser versionados con DVC.

---

### 7️.- Fase de costos y escalabilidad

- ChatGPT Plus sirve para desarrollo y prototipos.
- Si se decide integrar la API:
  - `gpt-5-turbo`: $0.005 / 1 000 tokens (entrada)
  - `gpt-5-turbo`: $0.015 / 1 000 tokens (salida)
- Estrategia recomendada:
  - Usar GPT-5 para generación de etiquetas iniciales.
  - Entrenar modelo propio (local) para ejecución masiva sin costo.

---

### 8️.- Conclusión

El sistema ARGOS avanza hacia una arquitectura híbrida:
- **Reglas expertas + Semántica + Aprendizaje.**
Esto permitirá automatizar la clasificación de materiales industriales manteniendo precisión técnica y trazabilidad de decisiones.

---

**Estado actual:** Pausado intencionalmente a la espera de retomarse.  
**Siguiente hito:** Definir formalmente las reglas expertas para la familia *VÁLVULAS*.
