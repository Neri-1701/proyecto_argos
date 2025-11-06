"""
ARGOS - Datos simulados de inventario para pruebas locales.

Este modulo crea un DataFrame en memoria con materiales de ejemplo.
No lee ni escribe archivos externos. Sirve como "fuente segura" de datos
para el MVP Hermes Alpha 0.1.0.

Columnas:
- COD_MATERIAL: Codigo unico del material
- DESCRIPCION_LARGA: Descripcion no estructurada del material
- FAMILIA: Familia general del material (valvula, empaque, esparrago, brida, junta)
"""

from __future__ import annotations

import pandas as pd


def load_inventory() -> pd.DataFrame:
    """
    Crea y devuelve un DataFrame simulado de inventario con 5-10 items.
    """
    data = [
        {
            "COD_MATERIAL": "3000001",
            "DESCRIPCION_LARGA": "Valvula de globo acero al carbono 2 pulgadas clase 600",
            "FAMILIA": "valvula",
        },
        {
            "COD_MATERIAL": "3000002",
            "DESCRIPCION_LARGA": "Valvula de bola acero inoxidable 1 pulgada clase 150",
            "FAMILIA": "valvula",
        },
        {
            "COD_MATERIAL": "3000003",
            "DESCRIPCION_LARGA": "Valvula compuerta PVC 1/2 pulgada clase 125",
            "FAMILIA": "valvula",
        },
        {
            "COD_MATERIAL": "3000004",
            "DESCRIPCION_LARGA": "Empaque de grafito expandido para brida 3 pulgadas",
            "FAMILIA": "empaque",
        },
        {
            "COD_MATERIAL": "3000005",
            "DESCRIPCION_LARGA": "Empaque PTFE para brida 1 pulgada ANSI 150",
            "FAMILIA": "empaque",
        },
        {
            "COD_MATERIAL": "3000006",
            "DESCRIPCION_LARGA": "Esparrago M12 acero al carbono zincado",
            "FAMILIA": "esparrago",
        },
        {
            "COD_MATERIAL": "3000007",
            "DESCRIPCION_LARGA": "Esparrago 3/4 UNC acero inoxidable",
            "FAMILIA": "esparrago",
        },
        {
            "COD_MATERIAL": "3000008",
            "DESCRIPCION_LARGA": "Brida A105 2 pulgadas clase 300 RF",
            "FAMILIA": "brida",
        },
        {
            "COD_MATERIAL": "3000009",
            "DESCRIPCION_LARGA": "Junta tipo anillo RTJ R45 para brida 6 pulgadas",
            "FAMILIA": "junta",
        },
    ]
    df = pd.DataFrame(data, columns=["COD_MATERIAL", "DESCRIPCION_LARGA", "FAMILIA"])
    return df


if __name__ == "__main__":
    df = load_inventory()
    print("Inventario simulado cargado.")
    print(df.head(10).to_string(index=False))

