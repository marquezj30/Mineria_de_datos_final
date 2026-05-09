import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("DATASET_MAESTRO_COVID_2020_2026.csv")

for anio in sorted(df['ANIO'].unique()):
    df_anio = df[df['ANIO'] == anio]
    
    # Regresión Logística simple para Diabetes
    X = sm.add_constant(df_anio['DIABETES'])
    model = sm.Logit(df_anio['FALLECIDO'], X).fit(disp=0)
    
    # El Odds Ratio es el exponencial de los coeficientes
    or_val = np.exp(model.params['DIABETES'])
    print(f"Año {anio} - Riesgo (Odds Ratio) por Diabetes: {or_val:.2f}")
    