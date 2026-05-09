import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("DATASET_MAESTRO_COVID_2020_2026.csv")

# Calcular mortalidad anual para personas con al menos una comorbilidad
df['TIENE_COMORBILIDAD'] = ((df['DIABETES'] == 1) | (df['HIPERTENSION'] == 1) | (df['OBESIDAD'] == 1)).astype(int)

tendencia = df.groupby(['ANIO', 'TIENE_COMORBILIDAD'])['FALLECIDO'].mean().unstack()

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(tendencia.index, tendencia[1], marker='o', label='Con Comorbilidad', color='red', linewidth=2)
plt.plot(tendencia.index, tendencia[0], marker='s', label='Sin Comorbilidad', color='green', linestyle='--')

plt.title('Evolución de la Mortalidad: 2020 - 2023')
plt.xlabel('Año')
plt.ylabel('Tasa de Letalidad (Promedio)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('grafico_tendencia.png')
plt.show()