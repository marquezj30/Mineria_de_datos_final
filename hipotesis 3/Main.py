import pandas as pd
import time
import os
from pathlib import Path

inicio = time.time()

if Path("covid_filtrado.csv.gz").exists():
    print("El dataset filtrado comprimido ya existe: covid_filtrado.csv.gz")
    print("Los scripts grafico1.py, grafico2.py y grafico3.py pueden leerlo directamente.")
    raise SystemExit(0)

# =========================
# ARCHIVOS
# =========================
archivos = [
    "COVID19MEXICO2020.csv",
    "COVID19MEXICO2021.csv",
    "COVID19MEXICO2022.csv",
    "COVID19MEXICO2023.csv",
    "COVID19MEXICO2024.csv"
]

faltantes = [archivo for archivo in archivos if not Path(archivo).exists()]
if faltantes:
    raise FileNotFoundError(
        "No se encontraron los CSV originales necesarios para regenerar covid_filtrado.csv: "
        + ", ".join(faltantes)
    )

# =========================
# COLUMNAS NECESARIAS
# =========================
columnas = [
    "FECHA_INGRESO",
    "FECHA_DEF",
    "INTUBADO",
    "EDAD",
    "DIABETES",
    "OBESIDAD",
    "EPOC",
    "TABAQUISMO",
    "HIPERTENSION",
    "CLASIFICACION_FINAL"
]

# =========================
# CONFIGURACIÓN
# =========================
tam_chunk = 50000
archivo_salida = "covid_filtrado.csv"

# borrar archivo previo
if os.path.exists(archivo_salida):
    os.remove(archivo_salida)

primer_archivo = True

# =========================
# PROCESAMIENTO
# =========================
for archivo in archivos:

    print(f"\nProcesando {archivo}...")

    for i, chunk in enumerate(pd.read_csv(
        archivo,
        usecols=columnas,
        chunksize=tam_chunk,
        low_memory=False
    )):

        # =========================
        # FILTRAR SOLO DATOS ÚTILES
        # =========================

        # clasificaciones válidas
        chunk = chunk[
            chunk["CLASIFICACION_FINAL"].isin([1,2,3,4,5,6,7])
        ]

        # edades válidas
        chunk = chunk[chunk["EDAD"] > 0]

        # intubado válido
        chunk = chunk[
            chunk["INTUBADO"].isin([1,2])
        ]

        # al menos una enfermedad
        chunk = chunk[
            (chunk["DIABETES"] == 1) |
            (chunk["OBESIDAD"] == 1) |
            (chunk["EPOC"] == 1) |
            (chunk["TABAQUISMO"] == 1) |
            (chunk["HIPERTENSION"] == 1)
        ]

        # =========================
        # GUARDAR
        # =========================
        chunk.to_csv(
            archivo_salida,
            mode="a",
            index=False,
            header=primer_archivo
        )

        primer_archivo = False

        print(f"Chunk {i+1} guardado")

    print(f"{archivo} completado ✅")

# =========================
# FINAL
# =========================
fin = time.time()

print("\n===================================")
print("CSV filtrado generado ✅")
print(f"Archivo: {archivo_salida}")
print(f"Tiempo: {fin - inicio:.2f} segundos")
print("===================================")
