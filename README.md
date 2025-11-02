# Sistema Inteligente de Clasificación y Localización de Materiales

**Autor:** Luis Felipe Neri Alvarado Fregoso

**Descripción:**  
Plantilla modular de Argos para clasificación jerárquica de materiales industriales.

---

## Estructura del proyecto

```
├── data/               <- Datos crudos, intermedios y procesados
├── notebooks/          <- Notebooks de exploración y entrenamiento
├── src/                <- Código fuente principal
│   ├── data/           <- Scripts de carga, limpieza y normalización
│   ├── features/       <- Ingeniería de características y extracción de atributos
│   ├── models/         <- Entrenamiento y predicción de modelos jerárquicos
│   └── visualization/  <- Gráficas y reportes visuales
├── reports/            <- Salidas generadas, métricas o logs
├── tests/              <- Unit tests
├── requirements.txt
├── dvc.yaml
└── README.md
```
---

## Cómo iniciar un nuevo proyecto Argos

```bash
cookiecutter path/a/cookiecutter-argos
```
