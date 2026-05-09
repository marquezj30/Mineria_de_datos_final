import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos limpios
df = pd.read_csv("DATASET_MAESTRO_COVID_2020_2026.csv")

# Crear una figura con dos subgráficos (2020 y 2024)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Mapa de calor para 2020
sns.heatmap(df[df['ANIO'] == 2020].corr(), annot=True, cmap='Reds', ax=ax1)
ax1.set_title('Asociación de Riesgo en 2020')

# Mapa de calor para 2024
sns.heatmap(df[df['ANIO'] == 2024].corr(), annot=True, cmap='Blues', ax=ax2)
ax2.set_title('Asociación de Riesgo en 2024')

plt.tight_layout()
plt.savefig('grafico_correlacion.png')
plt.show()