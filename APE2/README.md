# Práctica 02 - Simulación (UNL)

Comparación de modelos **determinísticos, estocásticos, discretos y continuos**
aplicados al crecimiento poblacional.

## Requisitos

- Python 3.x con el entorno virtual incluido en `venv/`
- Librerías: numpy, pandas, matplotlib, scipy (ver `requirements.txt`; no se
  instalan paquetes nuevos)

## Estructura

| Archivo | Descripción |
|---|---|
| `modelos.py` | Los 4 modelos (uno por función) + `estimar_r(datos)` |
| `comparacion.py` | Gráfica comparativa de los 4 modelos + datos reales |
| `experimentos.py` | Sensibilidad de los parámetros r, sigma y dt |
| `resultados/` | PNG de las gráficas y `comparacion.csv` |

## Parámetros

```python
datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]
P0    = datos[0] = 1000
T     = len(datos) - 1 = 6
r     = ln(datos[-1]/datos[0]) / (len(datos)-1) = ln(2.1)/6 ≈ 0.123656
sigma = 50      # desviación estándar del ruido normal
dt    = 0.1     # tamaño de paso del modelo continuo (Euler)
seed  = 42      # semilla fija con np.random.default_rng(seed)
```

## Ejecución

```bash
# Gráfica comparativa (guarda PNG en resultados/)
python comparacion.py

# Además muestra la figura con plt.show()
python comparacion.py --mostrar

# Experimentos de sensibilidad (r, sigma, dt)
python experimentos.py
python experimentos.py --mostrar
```

## Modelos (fórmulas de la guía)

1. **Determinístico:** `P(t) = P0 · e^(r·t)` — sin aleatoriedad.
2. **Discreto:** `P_{t+1} = P_t + r·P_t` — períodos 1..T, la lista inicia con P0.
3. **Estocástico:** `P_{t+1} = P_t + r·P_t + eps_t`, con `eps_t ~ N(0, σ²)`.
   Si la nueva población es negativa, se fija en **0**.
4. **Continuo (Euler):** `P_{t+dt} = P_t + dt·(r·P_t)`, con el vector de
   tiempo construido a partir de `dt`.

Cada función devuelve `(tiempo, poblacion)` como arreglos numpy.

## Resultados (`resultados/`)

- `comparacion.png` — 4 modelos + puntos de los datos reales
  (título, eje X "Tiempo", eje Y "Población", leyenda y cuadrícula).
- `comparacion.csv` — valores de los 4 modelos.
- `influencia_r.png` — crecimiento (r > 0) y decrecimiento (r < 0).
- `influencia_sigma.png` — σ = 25, 50, 100 con semilla fija.
- `influencia_dt.png` — dt = 1, 0.1, 0.05 contra la solución exacta.

## Interpretación matemática (resumen)

- **r** es la tasa exponencial: con `r > 0` la población crece
  (`e^(r·t)` se aleja de P0), con `r < 0` decae hacia 0; con `r = 0` el
  sistema queda en equilibrio (P constante = P0). A mayor |r|, más rápida
  la separación respecto de los datos.
- **Determinístico vs. discreto:** `P0·e^(rt)` es la solución continua de
  `dP/dt = r·P`; el discreto `P_t = P0·(1+r)^t` es su aproximación para r
  pequeño (`e^r ≈ 1 + r`), por eso diverge levemente al alejarse de t = 0.
- **Estocástico:** el ruido aditivo N(0, σ²) hace que cada trayectoria sea
  irregular alrededor de la tendencia; el truncamiento a 0 evita poblaciones
  negativas (imposibles biológicamente). Mayor σ ⇒ mayor dispersión.
- **Euler:** aproxima la solución exacta por rectas de pendiente `dt·r·P`;
  a menor **dt** la trayectoria converge a `P0·e^(rt)` (menor error de
  truncamiento), a mayor dt se aleja (con dt = 1 se nota el sesgo).
- Los datos reales quedan entre el determinístico y el discreto: los modelos
  capturan bien la tendencia exponencial observada.
