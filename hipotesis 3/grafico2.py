import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from pathlib import Path

# 1. Cargar datos
csv_path = Path("covid_filtrado.csv")
if not csv_path.exists():
    csv_path = Path("covid_filtrado.csv.gz")

df = pd.read_csv(csv_path, low_memory=False)

# 2. Preparar los tiempos (Días desde ingreso hasta defunción)
df['FECHA_INGRESO'] = pd.to_datetime(df['FECHA_INGRESO'])
df['FECHA_DEF'] = pd.to_datetime(df['FECHA_DEF'], errors='coerce')

# Creamos la columna de "Evento" (1 si falleció, 0 si no)
df['EVENTO'] = df['FECHA_DEF'].notna().astype(int)

# Calculamos los días. Si no murió, ponemos un tiempo de seguimiento (ej. 30 días)
df['DIAS'] = (df['FECHA_DEF'] - df['FECHA_INGRESO']).dt.days
df['DIAS'] = df['DIAS'].fillna(30) # Asumimos 30 días para los que sobrevivieron
df.loc[df['DIAS'] < 0, 'DIAS'] = 0 # Limpieza de errores en fechas

# 3. Separar los grupos
grupo_covid = df[df['CLASIFICACION_FINAL'].isin([1, 2, 3])]
grupo_no_covid = df[~df['CLASIFICACION_FINAL'].isin([1, 2, 3])]

# 4. Crear el gráfico
kmf = KaplanMeierFitter()
plt.figure(figsize=(10, 6))

# Curva para COVID+
kmf.fit(grupo_covid['DIAS'], event_observed=grupo_covid['EVENTO'], label='Pacientes COVID+')
kmf.plot_survival_function(color='red')

# Curva para No-COVID
kmf.fit(grupo_no_covid['DIAS'], event_observed=grupo_no_covid['EVENTO'], label='Pacientes Otros (No-COVID)')
kmf.plot_survival_function(color='blue')

plt.title('Curva de Supervivencia: COVID-19 vs Otras Afecciones Respiratorias')
plt.xlabel('Días desde el ingreso al hospital')
plt.ylabel('Probabilidad de Supervivencia')
plt.grid(True, alpha=0.3)
plt.savefig('supervivencia_kaplan_meier.png')
plt.show()
