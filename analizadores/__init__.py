"""Cadena de analizadores.

Cada módulo expone:
    NOMBRE    -> str
    COLUMNAS  -> list[str] con las columnas que aporta a la tabla
    analizar(y, sr) -> dict {columna: valor}

Para añadir uno nuevo: crear el módulo y agregarlo a ANALIZADORES.
"""
from . import bpm

ANALIZADORES = [bpm]
