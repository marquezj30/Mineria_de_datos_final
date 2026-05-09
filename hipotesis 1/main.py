import pandas as pd
import glob
import os
from pathlib import Path

if Path("DATASET_MAESTRO_COVID_2020_2026.csv.gz").exists():
    print("El dataset limpio comprimido ya existe: DATASET_MAESTRO_COVID_2020_2026.csv.gz")
    print("Los scripts de analisis pueden leerlo directamente; no es necesario regenerarlo.")
    raise SystemExit(0)

# 1. Identificar todos los archivos que empiecen con 'COVID19MEXICO'
# Asegúrate de ejecutar este script en la misma carpeta donde están tus CSVs
archivos = glob.glob("COVID19MEXICO20*.csv")
archivos.sort() # Los ordena de 2020 a 2026

if not archivos:
    raise FileNotFoundError(
        "No se encontraron archivos COVID19MEXICO20*.csv. "
        "Para regenerar el dataset maestro se necesitan los CSV originales."
    )

lista_df_limpios = []

print(f"Archivos detectados: {archivos}")

for archivo in archivos:
    print(f"Procesando: {archivo}...")
    
    # Cargar archivo (usamos chunksize si los archivos son muy pesados, o normal)
    df = pd.read_csv(archivo, low_memory=False)
    
    # --- PROCESO DE LIMPIEZA ---
    
    # A. Filtro COVID (Clasificación 1, 2, 3)
    df = df[df['CLASIFICACION_FINAL'].isin([1, 2, 3])].copy()
    
    # B. Crear variable de Fallecido (0/1)
    df['FALLECIDO'] = (df['FECHA_DEF'] != '9999-99-99').astype(int)
    
    # C. Extraer Año del nombre del archivo o de FECHA_SINTOMAS
    # Extraemos el año directamente de la columna para mayor precisión
    df['ANIO'] = pd.to_datetime(df['FECHA_SINTOMAS'], errors='coerce').dt.year
    
    # D. Limpiar comorbilidades (Diabetes, Hipertensión, Obesidad)
    comorb = ['DIABETES', 'HIPERTENSION', 'OBESIDAD']
    for c in comorb:
        # Solo registros con 1 (Sí) o 2 (No)
        df = df[df[c].isin([1, 2])]
        # Convertir 2 (No) a 0
        df[c] = df[c].replace(2, 0)
    
    # E. Seleccionar solo lo necesario para ahorrar memoria
    columnas = ['ANIO', 'FALLECIDO', 'DIABETES', 'HIPERTENSION', 'OBESIDAD', 'ENTIDAD_RES']
    lista_df_limpios.append(df[columnas])

# 2. Unir todos los años en un solo DataFrame
df_final = pd.concat(lista_df_limpios, ignore_index=True)

# 3. Guardar el resultado final
df_final.to_csv("DATASET_MAESTRO_COVID_2020_2026.csv", index=False)

print("-" * 30)
print("¡PROCESO EXITOSO!")
print(f"Total de registros procesados: {len(df_final)}")
print(f"Años incluidos: {df_final['ANIO'].unique()}")
