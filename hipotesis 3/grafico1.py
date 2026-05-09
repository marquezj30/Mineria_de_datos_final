import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

# 1. Cargar el dataset nuevo
try:
    csv_path = Path("covid_filtrado.csv")
    if not csv_path.exists():
        csv_path = Path("covid_filtrado.csv.gz")

    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Dataset '{csv_path.name}' cargado correctamente.")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'covid_filtrado.csv' ni 'covid_filtrado.csv.gz'")
    exit()

# 2. Preprocesamiento de Variables
# INTUBADO: 1=Sí, 2=No. Convertimos 2 a 0 (No) y filtramos basura (97, 98, 99)
df = df[df['INTUBADO'].isin([1, 2])].copy()
df['INTUBADO'] = df['INTUBADO'].replace(2, 0)

# Comorbilidades: Convertir 2 (No) a 0. Mantener 1 (Sí).
comorb = ['DIABETES', 'EPOC', 'HIPERTENSION', 'OBESIDAD', 'TABAQUISMO']
for c in comorb:
    df = df[df[c].isin([1, 2])] # Solo registros válidos
    df[c] = df[c].replace(2, 0)

# 3. Separar Grupos (Basado en CLASIFICACION_FINAL)
# Grupo A: COVID+ (1, 2, 3) | Grupo B: Otros Respiratorios (6, 7, etc.)
grupo_covid = df[df['CLASIFICACION_FINAL'].isin([1, 2, 3])].copy()
grupo_control = df[~df['CLASIFICACION_FINAL'].isin([1, 2, 3])].copy()

variables_x = ['EDAD', 'DIABETES', 'EPOC', 'HIPERTENSION', 'OBESIDAD', 'TABAQUISMO']

def calcular_importancia(data, nombre_grupo):
    if data.empty: return None
    X = data[variables_x]
    y = data['INTUBADO']
    
    # Entrenamos el modelo de importancia
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    imp = pd.DataFrame({'Variable': variables_x, 'Importancia': model.feature_importances_})
    return imp.sort_values(by='Importancia', ascending=False)

# Ejecutar análisis
imp_covid = calcular_importancia(grupo_covid, "COVID+")
imp_control = calcular_importancia(grupo_control, "No-COVID")

# 4. Visualización Comparativa
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), sharex=True)

sns.barplot(data=imp_covid, x='Importancia', y='Variable', ax=ax1, palette='OrRd_r')
ax1.set_title('Pesos Predictivos: GRUPO COVID+\n(Quién termina en ventilador)')

sns.barplot(data=imp_control, x='Importancia', y='Variable', ax=ax2, palette='GnBu_r')
ax2.set_title('Pesos Predictivos: GRUPO NO-COVID\n(Otras afecciones respiratorias)')

plt.tight_layout()
plt.savefig('importancia_hipotesis_4.png', dpi=300)
plt.show()

# Resumen numérico para tu reporte
print("\n--- RESULTADOS PARA TU HIPÓTESIS ---")
print("Top 3 Predictores COVID+:\n", imp_covid.head(3))
print("\nTop 3 Predictores No-COVID:\n", imp_control.head(3))
