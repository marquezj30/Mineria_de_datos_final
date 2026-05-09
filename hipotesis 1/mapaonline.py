import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Cargar tus datos
try:
    csv_path = Path("DATASET_MAESTRO_COVID_2020_2026.csv")
    if not csv_path.exists():
        csv_path = Path("DATASET_MAESTRO_COVID_2020_2026.csv.gz")

    df = pd.read_csv(csv_path)
    print("Dataset cargado correctamente.")
except FileNotFoundError:
    print("Error: No se encontró el archivo.")
    exit()

# 2. Descargar el mapa
url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
print("Descargando mapa de México...")
mexico = gpd.read_file(url)

# 3. DICCIONARIO DE MAPEO (Crucial para corregir el error de 'MX-ZAC')
# Este diccionario convierte los códigos del mapa 'id' a los números de ENTIDAD_RES
mapeo_estados = {
    'MX-AGU': 1, 'MX-BCN': 2, 'MX-BCS': 3, 'MX-CAM': 4, 'MX-COA': 5,
    'MX-COL': 6, 'MX-CHP': 7, 'MX-CHH': 8, 'MX-CMX': 9, 'MX-DUR': 10,
    'MX-GUA': 11, 'MX-GRO': 12, 'MX-HID': 13, 'MX-JAL': 14, 'MX-MEX': 15,
    'MX-MIC': 16, 'MX-MOR': 17, 'MX-NAY': 18, 'MX-NLE': 19, 'MX-OAX': 20,
    'MX-PUE': 21, 'MX-QUE': 22, 'MX-ROO': 23, 'MX-SLP': 24, 'MX-SIN': 25,
    'MX-SON': 26, 'MX-TAB': 27, 'MX-TAM': 28, 'MX-TLA': 29, 'MX-VER': 30,
    'MX-YUC': 31, 'MX-ZAC': 32
}

# Aplicamos el mapeo al mapa descargado
mexico['id_numerico'] = mexico['id'].map(mapeo_estados)

# 4. Preparar datos (Año 2020)
mapa_data = df[df['ANIO'] == 2020].groupby('ENTIDAD_RES')['FALLECIDO'].mean().reset_index()

# 5. Unir los datos usando la nueva columna numérica
merged = mexico.merge(mapa_data, left_on="id_numerico", right_on="ENTIDAD_RES")

# 6. Graficar
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
merged.plot(
    column='FALLECIDO', 
    cmap='YlOrRd', 
    legend=True, 
    ax=ax, 
    edgecolor='0.3',
    linewidth=0.5,
    legend_kwds={'label': "Tasa de Letalidad", 'orientation': "horizontal", 'pad': 0.05}
)

plt.title('Distribución de Mortalidad por COVID-19 (2020)', fontsize=16)
plt.axis('off')
plt.savefig('mapa_final.png', dpi=300)
print("¡Éxito! Mapa generado sin errores de base 10.")
plt.show()
