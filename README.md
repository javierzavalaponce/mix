# Biblioteca DJ

Analiza una carpeta de canciones y las explora en una tabla en la terminal.

- `orquestador.py` corre una cadena de analizadores (hoy: BPM) y genera `biblioteca.csv`.
- `explorar.py` abre `biblioteca.csv` en una tabla navegable (Textual).

## Requisitos

- Python 3.12 o superior (lo exigen `librosa` y `numpy`).
- Probado en Linux. Las versiones de `requirements.txt` están fijadas, así que en
  otra plataforma (ARM, macOS) puede que alguna no exista.

## Instalación

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Uso

Analizar las canciones de la carpeta (necesita los `.mp3` aquí):

```bash
.venv/bin/python orquestador.py              # todos los analizadores
.venv/bin/python orquestador.py --solo bpm   # solo algunos
.venv/bin/python orquestador.py --rehacer    # recalcula aunque ya exista el dato
```

Es incremental: solo calcula lo que falta en `biblioteca.csv`.

Explorar el resultado (solo necesita `biblioteca.csv`, no los audios):

```bash
.venv/bin/python explorar.py
```

Salir con `Ctrl+Q`.

## Notas

- Los `.mp3` no se versionan (están en `.gitignore`). Hay que copiarlos aparte
  al otro equipo si quieres volver a analizar.
- La primera ejecución del análisis es más lenta porque `numba` compila al primer uso.
- Leer la tabla en pandas: `pd.read_csv("biblioteca.csv", index_col="archivo")`.

## Añadir un analizador

1. Crear `analizadores/nombre.py` con `NOMBRE`, `COLUMNAS` y `analizar(y, sr)`,
   que devuelve un dict `{columna: valor}`.
2. Registrarlo en la lista `ANALIZADORES` de `analizadores/__init__.py`.
3. Ejecutar `orquestador.py`: solo calcula las columnas nuevas.
