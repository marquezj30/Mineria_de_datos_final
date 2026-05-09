import pandas as pd
import plotly.express as px
import requests
from pathlib import Path

# 1. Cargar datos
csv_path = Path("DATASET_MAESTRO_COVID_2020_2026.csv")
if not csv_path.exists():
    csv_path = Path("DATASET_MAESTRO_COVID_2020_2026.csv.gz")

df = pd.read_csv(csv_path)

# 2. Descargar el GeoJSON
url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
mexico_geo = requests.get(url).json()

# 3. DICCIONARIO INVERSO: Convertir tus números a los códigos del mapa (MX-XXX)
inv_mapeo = {
    1: 'MX-AGU', 2: 'MX-BCN', 3: 'MX-BCS', 4: 'MX-CAM', 5: 'MX-COA',
    6: 'MX-COL', 7: 'MX-CHP', 8: 'MX-CHH', 9: 'MX-CMX', 10: 'MX-DUR',
    11: 'MX-GUA', 12: 'MX-GRO', 13: 'MX-HID', 14: 'MX-JAL', 15: 'MX-MEX',
    16: 'MX-MIC', 17: 'MX-MOR', 18: 'MX-NAY', 19: 'MX-NLE', 20: 'MX-OAX',
    21: 'MX-PUE', 22: 'MX-QUE', 23: 'MX-ROO', 24: 'MX-SLP', 25: 'MX-SIN',
    26: 'MX-SON', 27: 'MX-TAB', 28: 'MX-TAM', 29: 'MX-TLA', 30: 'MX-VER',
    31: 'MX-YUC', 32: 'MX-ZAC'
}

# Aplicamos el código de texto a tus datos para que Plotly los encuentre en el JSON
df['CODIGO_MAPA'] = df['ENTIDAD_RES'].map(inv_mapeo)

# 4. Preparar los datos para las comorbilidades
df['CUALQUIERA'] = ((df['DIABETES'] == 1) | (df['HIPERTENSION'] == 1) | (df['OBESIDAD'] == 1)).astype(int)

opciones = ['DIABETES', 'HIPERTENSION', 'OBESIDAD', 'CUALQUIERA']
df_plot_list = []

for enfermedad in opciones:
    # Agrupamos incluyendo la nueva columna CODIGO_MAPA
    temp = df[df[enfermedad] == 1].groupby(['ANIO', 'CODIGO_MAPA'])['FALLECIDO'].mean().reset_index()
    temp['ENFERMEDAD'] = enfermedad
    df_plot_list.append(temp)

df_final_mapa = pd.concat(df_plot_list)

# 5. Crear el Mapa Interactivo
fig = px.choropleth(
    df_final_mapa,
    geojson=mexico_geo,
    locations="CODIGO_MAPA",  # Usamos el código MX-XXX
    featureidkey="id",        # En el JSON, el campo se llama 'id'
    color="FALLECIDO",
    animation_frame="ANIO",
    facet_col="ENFERMEDAD",
    color_continuous_scale="YlOrRd",
    range_color=[0, 0.25],    # Ajustamos escala para ver mejor los cambios
    labels={'FALLECIDO': 'Letalidad'}
)

# 6. Ajustar visualización y enfoque
fig.update_geos(
    visible=False, 
    fitbounds="locations"
)

fig.update_layout(
    title_text='Análisis de Letalidad COVID-19 (2020-2026)',
    height=500
)

# Guardar
fig.write_html("mapa_interactivo_covid.html")
print("¡Listo! Si el mapa estaba en blanco, ahora debería tener color.")
