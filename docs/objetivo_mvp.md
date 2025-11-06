# Objetivo del MVP – ARGOS Alpha 0.1.0 (“Hermes”)

## Descripción general
El MVP de ARGOS tiene como finalidad validar la capacidad del sistema para identificar materiales industriales a partir de descripciones largas proporcionadas por el usuario.  

Esta versión inicial busca consolidar la arquitectura jerárquica de clasificación y demostrar su precisión en un conjunto de pruebas controladas.

---

## Objetivo general
A partir de una descripción no estructurada de un material (por ejemplo, extraída de un plano isométrico), el sistema debe **identificar el material en inventario que mejor se adecue a lo solicitado** y devolver su **código de material** y **descripción estándar** correspondiente.

El objetivo de desempeño para esta versión es alcanzar un **90 % de acierto** en los casos de prueba.

---

## Objetivos específicos

1. **Normalización de texto:**  
   - Convertir el texto a mayúsculas, eliminar caracteres especiales y unificar unidades.  
   - Extraer parámetros relevantes: tipo, diámetro nominal, clase, norma, material base.

2. **Clasificación jerárquica (nivel 1):**  
   - Identificar la familia de material (válvula, brida, espárrago, empaque, etc.).  
   - Usar modelos ligeros de clasificación basados en texto.

3. **Búsqueda semántica:**  
   - Aplicar técnicas de similitud textual (TF-IDF, embeddings o fuzzy matching).  
   - Filtrar los resultados por familia para obtener coincidencias precisas.  

4. **Evaluación del desempeño:**  
   - Comparar predicciones contra un set de referencia.  
   - Calcular métricas de precisión, recall y F1-score.  

5. **Interfaz CLI:**  
   - Permitir al usuario ingresar descripciones y recibir la sugerencia más probable.  
   - Mostrar descripción estándar, código y nivel de confianza.  

---

## Alcance técnico

- Entradas: texto libre en español con descripción técnica.  
- Salidas: código de material y descripción estándar más probable.  
- Evaluación mínima: 90 % de acierto en top-1 (predicción principal).  
- Lenguaje: Python 3.12+.  
- Librerías principales: `pandas`, `scikit-learn`, `fuzzywuzzy` o `rapidfuzz`.  

---

## Entregables

- Código fuente organizado por módulos (`src/`).  
- Dataset de prueba etiquetado (`data/processed/`).  
- Notebook experimental (`notebooks/argos_alpha_experiments.ipynb`).  
- Reporte de resultados.  

---

## Futuras extensiones
- Nivel 2 del modelo jerárquico (subclasificación dentro de la familia).  
- Integración con inventarios reales (SAP export).  
- Interfaz web y localización geográfica de materiales.  
