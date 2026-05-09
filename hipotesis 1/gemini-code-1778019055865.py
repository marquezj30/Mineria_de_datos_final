import pandas as pd
import plotly.express as px
import json
import requests

# 1. Cargar datos
df = pd.read_csv("DATASET_MAESTRO_COVID_2020_2026.csv")

# 2. Descargar el GeoJSON para Plotly
url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
mexico_geo = requests.get(url).json()

# 3. Preparar los datos: Calcular mortalidad promedio por Estado, Año y Enfermedad
# Vamos a crear una columna que nos diga si el paciente tiene "Cualquier comorbilidad"
df['CUALQUIERA'] = ((df['DIABETES'] == 1) | (df['HIPERTENSION'] == 1) | (df['OBESIDAD'] == 1)).astype(int)

# Agrupamos para tener la tasa de mortalidad según la condición
opciones = ['DIABETES', 'HIPERTENSION', 'OBESIDAD', 'CUALQUIERA']
df_plot = []

for enfermedad in opciones:
    # Solo tomamos a los que SÍ tienen la enfermedad (valor 1)
    temp = df[df[enfermedad] == 1].groupby(['ANIO', 'ENTIDAD_RES'])['FALLECIDO'].mean().reset_index()
    temp['ENFERMEDAD'] = enfermedad
    df_plot.append(temp)

df_final_mapa = pd.concat(df_plot)

# 4. Crear el Mapa Interactivo con PLOTLY
fig = px.choropleth(
    df_final_mapa,
    geojson=mexico_geo,
    locations="ENTIDAD_RES",      # Columna del ID en el CSV
    featureidkey="properties.id", # Ruta del ID en el JSON (ajustado a este JSON específico)
    color="FALLECIDO",
    animation_frame="ANIO",       # ¡Barra de tiempo abajo!
    facet_col="ENFERMEDAD",       # Crea mapas separados por enfermedad
    color_continuous_scale="YlOrRd",
    range_color=[0, 0.3],         # Escala fija para notar la disminución real
    scope="mexico",
    labels={'FALLECIDO': 'Tasa de Letalidad'}
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_text='Evolución de Letalidad COVID-19 por Comorbilidad (2020-2026)')

# 5. Guardar como HTML
fig.write_html("mapa_interactivo_covid.html")
print("¡Listo! Abre 'mapa_interactivo_covid.html' en tu navegador.")