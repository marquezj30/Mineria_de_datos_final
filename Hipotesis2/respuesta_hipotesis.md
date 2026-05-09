# Respuesta a la hipotesis

## Pregunta

¿El retraso entre la aparicion de sintomas y el ingreso hospitalario representa un factor de riesgo mas importante para la mortalidad que antecedentes respiratorios como asma o tabaquismo?

## Datos usados

El analisis se ejecuto directamente desde `covid19_limpio.csv` o su version comprimida `covid19_limpio.csv.gz`, que contiene los casos confirmados de COVID-19 ya integrados, depurados y reducidos a las variables necesarias para esta hipotesis.

- Filas limpias analizadas: 7,669,425
- Defunciones registradas: 333,464
- Mortalidad global: 4.35%

## Mortalidad observada por retraso

- 0-2 dias: 2.19% (88,435 muertes / 4,039,396 casos)
- 3-5 dias: 4.02% (102,519 muertes / 2,548,261 casos)
- 6-10 dias: 11.92% (108,707 muertes / 912,193 casos)
- 11+ dias: 19.93% (33,803 muertes / 169,575 casos)

## Mortalidad por retraso y perfil respiratorio

- 0-2 dias / Sin tabaquismo ni asma: 2.15% (81,296 muertes / 3,776,260 casos)
- 0-2 dias / Solo tabaquismo: 3.02% (5,762 muertes / 190,964 casos)
- 0-2 dias / Solo asma: 1.82% (1,229 muertes / 67,559 casos)
- 0-2 dias / Tabaquismo + asma: 3.21% (148 muertes / 4,613 casos)
- 3-5 dias / Sin tabaquismo ni asma: 3.96% (93,270 muertes / 2,355,257 casos)
- 3-5 dias / Solo tabaquismo: 5.20% (7,358 muertes / 141,563 casos)
- 3-5 dias / Solo asma: 3.57% (1,711 muertes / 47,968 casos)
- 3-5 dias / Tabaquismo + asma: 5.18% (180 muertes / 3,473 casos)
- 6-10 dias / Sin tabaquismo ni asma: 11.84% (98,528 muertes / 832,135 casos)
- 6-10 dias / Solo tabaquismo: 13.65% (8,330 muertes / 61,040 casos)
- 6-10 dias / Solo asma: 9.53% (1,671 muertes / 17,531 casos)
- 6-10 dias / Tabaquismo + asma: 11.97% (178 muertes / 1,487 casos)
- 11+ dias / Sin tabaquismo ni asma: 19.79% (30,353 muertes / 153,363 casos)
- 11+ dias / Solo tabaquismo: 22.62% (2,834 muertes / 12,530 casos)
- 11+ dias / Solo asma: 16.35% (552 muertes / 3,376 casos)
- 11+ dias / Tabaquismo + asma: 20.92% (64 muertes / 306 casos)

## Visualizaciones generadas

- `figuras/heatmap_mortalidad_retraso_perfil.png`
- `figuras/mortalidad_por_retraso_simple.png`

## Conclusion

El analisis respalda la hipotesis: el retraso entre la aparicion de sintomas y el ingreso hospitalario representa un factor de riesgo mas importante para la mortalidad por COVID-19 que los antecedentes respiratorios evaluados, como asma y tabaquismo. La mortalidad aumenta de forma clara conforme crecen los dias de demora, pasando de niveles bajos en atenciones tempranas a porcentajes mucho mas altos en pacientes atendidos despues de 11 dias o mas. Aunque el tabaquismo puede elevar el riesgo dentro de algunos grupos, su efecto es menor frente al impacto acumulado del retraso. Por ello, la evidencia principal del trabajo indica que la atencion temprana fue determinante para reducir el riesgo de defuncion.
