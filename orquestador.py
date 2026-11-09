"""Orquestador: corre la cadena de analizadores y construye biblioteca.csv.

Uso:
    python orquestador.py              # todos los analizadores
    python orquestador.py --solo bpm   # solo algunos
    python orquestador.py --rehacer    # recalcula aunque ya exista el dato
"""
import argparse
import sys
from pathlib import Path

import librosa
import pandas as pd

from analizadores import ANALIZADORES

SALIDA = Path("biblioteca.csv")
EXTENSIONES = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}


def descubrir_archivos():
    return sorted(
        p.name for p in Path(".").iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONES
    )


def cargar_tabla():
    if SALIDA.exists():
        return pd.read_csv(SALIDA, index_col="archivo")
    return pd.DataFrame(index=pd.Index([], name="archivo"))


def pendiente(tabla, archivo, analizador, rehacer):
    """True si falta algún dato de este analizador para este archivo."""
    if rehacer or archivo not in tabla.index:
        return True
    for col in analizador.COLUMNAS:
        if col not in tabla.columns or pd.isna(tabla.at[archivo, col]):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", nargs="+", help="nombres de analizadores a correr")
    ap.add_argument("--rehacer", action="store_true")
    args = ap.parse_args()

    analizadores = [a for a in ANALIZADORES if not args.solo or a.NOMBRE in args.solo]
    if not analizadores:
        sys.exit(f"Ningún analizador coincide con {args.solo}")

    tabla = cargar_tabla()
    archivos = descubrir_archivos()

    for archivo in archivos:
        trabajo = [a for a in analizadores if pendiente(tabla, archivo, a, args.rehacer)]
        if not trabajo:
            print(f"= {archivo} (al día)")
            continue

        # El audio se carga una sola vez y se comparte entre analizadores.
        try:
            y, sr = librosa.load(archivo)
        except Exception as e:
            print(f"! {archivo}: no se pudo cargar ({e})", file=sys.stderr)
            continue

        for a in trabajo:
            try:
                for col, valor in a.analizar(y, sr).items():
                    tabla.loc[archivo, col] = valor
                print(f"+ {archivo} [{a.NOMBRE}]")
            except Exception as e:
                print(f"! {archivo} [{a.NOMBRE}]: {e}", file=sys.stderr)

        tabla.to_csv(SALIDA)  # guardado incremental: si se corta, no se pierde nada

    # Archivos que ya no existen en la carpeta se conservan en la tabla.
    tabla.sort_index().to_csv(SALIDA)
    print(f"\n{len(tabla)} archivos en {SALIDA}")


if __name__ == "__main__":
    main()
