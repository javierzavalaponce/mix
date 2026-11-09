import csv
from pathlib import Path

CARPETA = Path(".")
CATALOGO = CARPETA / "biblioteca.csv"
SALIDA = CARPETA / "seleccion.m3u"


def crear_playlist():
    with CATALOGO.open(encoding="utf-8", newline="") as f:
        canciones = csv.DictReader(f)

        with SALIDA.open("w", encoding="utf-8") as lista:
            lista.write("#EXTM3U\n")

            for cancion in canciones:
                archivo = CARPETA / cancion["archivo"]

                if archivo.is_file():
                    lista.write(f"{archivo.resolve()}\n")

    print(f"Playlist creada: {SALIDA}")


if __name__ == "__main__":
    crear_playlist()



