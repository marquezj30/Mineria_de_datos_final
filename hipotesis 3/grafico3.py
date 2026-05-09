import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Cargar datos
csv_path = Path("covid_filtrado.csv")
if not csv_path.exists():
    csv_path = Path("covid_filtrado.csv.gz")

df = pd.read_csv(csv_path, low_memory=False)

# 2. Filtrar solo pacientes que FUERON intubados (INTUBADO == 1)
# Queremos ver el perfil de edad de quienes ocuparon el recurso crítico
df_intubados = df[df['INTUBADO'] == 1].copy()

# 3. Crear columna de Grupo para comparar
df_intubados['GRUPO'] = df_intubados['CLASIFICACION_FINAL'].apply(
    lambda x: 'COVID+' if x in [1, 2, 3] else 'NO-COVID'
)

# 4. Crear el gráfico de violín
plt.figure(figsize=(12, 7))
sns.violinplot(x='GRUPO', y='EDAD', data=df_intubados, palette={'COVID+': 'red', 'NO-COVID': 'blue'}, inner="quartile")

plt.title('Distribución de Edades en Pacientes Intubados\n(Perfil de uso de ventiladores)')
plt.xlabel('Grupo de Diagnóstico')
plt.ylabel('Edad del Paciente')
plt.grid(axis='y', alpha=0.3)

plt.savefig('violin_edad_intubados.png')
plt.show()
