# ARGOS – Sistema Inteligente de Clasificación y Localización de Materiales  
**Versión:** Alpha 0.1.0  
**Nombre clave:** Hermes  
**Repositorio:** `proyecto_argos/argos_materiales`

---

## Descripción general

ARGOS es un sistema inteligente diseñado para **clasificar y localizar materiales industriales** a partir de descripciones no estructuradas, como las provenientes de planos isométricos, requisiciones o reportes de campo.

La versión **Alpha 0.1.0 (Hermes)** constituye el primer prototipo funcional, enfocado en demostrar la capacidad del sistema para **reconocer la familia del material y sugerir el código más adecuado disponible en inventario** con una precisión objetivo del 90 %.

---

## Objetivo general

Desarrollar un prototipo capaz de, a partir de una **descripción larga** proporcionada por el usuario, identificar el **material en inventario** que mejor se adecue a lo solicitado, devolviendo su **descripción estándar** y **código de material**.

---

## Objetivos específicos

1. **Entrada:** recibir una descripción textual libre del usuario.  
2. **Preprocesamiento:** normalizar texto y extraer tokens relevantes (tipo, diámetro, clase, norma, material).  
3. **Clasificación primaria:** determinar la familia del material mediante un modelo jerárquico (nivel 1).  
4. **Búsqueda semántica:** aplicar comparación de similitud dentro del inventario de esa familia.  
5. **Salida:** mostrar la descripción y código del material más probable junto con su puntaje de similitud.  
6. **Evaluación:** alcanzar ≥ 90 % de coincidencia en pruebas controladas.

---

## Alcance del MVP (Alpha 0.1.0)

Incluye:
- Preprocesamiento textual.  
- Clasificador de familia (modelo jerárquico nivel 1).  
- Búsqueda semántica por similitud textual.  
- Interfaz de línea de comandos (CLI) para pruebas.

No incluye:
- Localización física de materiales.  
- Conexión con SAP u otros sistemas externos.  
- Dashboard o interfaz web.

---

## Estructura del proyecto

```text
argos_materiales/
│
├── data/
│   ├── raw/                     # Datos originales (extracciones SAP, textos brutos)
│   ├── processed/               # Datos preprocesados listos para entrenamiento
│   └── inventory_sample.csv     # Muestra representativa del inventario
│
├── docs/
│   └── objetivo_mvp.md          # Documento con los objetivos técnicos del MVP
│
├── notebooks/
│   └── argos_alpha_experiments.ipynb   # Experimentos y pruebas del modelo Alpha
│
├── src/
│   ├── preprocess.py            # Limpieza, normalización y tokenización de texto
│   ├── classify_family.py       # Clasificador jerárquico de familia
│   ├── search_material.py       # Motor de búsqueda por similitud
│   └── main.py                  # Script principal del MVP
│
├── tests/
│   └── test_argos_alpha.py      # Pruebas unitarias del prototipo
│
├── .gitignore
├── requirements.txt             # Dependencias del entorno virtual
├── VERSION                      # Archivo de control de versión (0.1.0)
└── README.md                    # Descripción general del proyecto
```
---

## Licencia

Uso interno y académico bajo los lineamientos del proyecto **ARGOS**.  
Desarrollado por **Luis Felipe Neri Alvarado Fregoso** como parte del proyecto de investigación aplicada **Sistema Inteligente de Clasificación y Localización de Materiales**.

---

## Créditos

**Desarrollo:**  
Luis Felipe Neri Alvarado Fregoso

---

## Historial de versiones

- **Alpha 0.1.0 – Hermes (2025-11-06)**  
  - Definición del objetivo general.  
  - Creación de estructura base del repositorio.  
  - Implementación prevista de los módulos: `preprocess`, `classify_family`, `search_material`.
