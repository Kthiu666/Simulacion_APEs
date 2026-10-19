"""Modelos de crecimiento poblacional (Práctica 02 - Simulación).

Cuatro enfoques para modelar el crecimiento de una población:
  1. Determinístico: P(t) = P0 * e^(r t)
  2. Discreto:       P_{t+1} = P_t + r * P_t
  3. Estocástico:    P_{t+1} = P_t + r * P_t + eps_t,  eps_t ~ N(0, sigma^2)
                     (si la nueva población < 0, se fija en 0)
  4. Continuo (Euler): P_{t+dt} = P_t + dt * (r * P_t)

Cada función devuelve (tiempo, poblacion) como arreglos numpy.
"""

import numpy as np

# Datos de entrada obligatorios de la práctica
datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]

# Parámetros por defecto de la práctica
P0_DEFECTO = datos[0]          # población inicial
T_DEFECTO = len(datos) - 1     # 6 períodos
SIGMA_DEFECTO = 50             # desviación estándar del ruido
DT_DEFECTO = 0.1               # tamaño de paso del modelo continuo


def estimar_r(datos):
    """Estima la tasa de crecimiento r a partir de los datos observados.

    Usa la fórmula de la guía:
        r = ln(datos[-1] / datos[0]) / (len(datos) - 1)

    Parámetros:
        datos (list or array): serie de poblaciones observadas (>= 2 valores).

    Retorna:
        float: tasa de crecimiento estimada r.
    """
    if len(datos) < 2:
        raise ValueError("Se necesitan al menos 2 datos para estimar r.")
    return np.log(datos[-1] / datos[0]) / (len(datos) - 1)


def modelo_deterministico(P0, r, tiempo, n_puntos=100):
    """Modelo determinístico: P(t) = P0 * e^(r t). Sin aleatoriedad.

    Parámetros:
        P0 (float): población inicial.
        r (float): tasa de crecimiento.
        tiempo (array_like): vector de tiempo de referencia (de 0 a T).
        n_puntos (int): cantidad de puntos del vector de tiempo resultante.

    Retorna:
        tuple: (tiempo, poblacion) como arreglos numpy.
    """
    t = np.linspace(tiempo[0], tiempo[-1], n_puntos)
    poblacion = P0 * np.exp(r * t)
    return t, poblacion


def modelo_discreto(P0, r, tiempo):
    """Modelo discreto: P_{t+1} = P_t + r * P_t, por períodos.

    La lista de poblaciones inicia con P0 y se itera un paso por cada
    elemento adicional del vector de tiempo (períodos 1..T).

    Parámetros:
        P0 (float): población inicial.
        r (float): tasa de crecimiento.
        tiempo (array_like): vector de períodos (0 a T).

    Retorna:
        tuple: (tiempo, poblacion) como arreglos numpy.
    """
    tiempo = np.asarray(tiempo, dtype=float)
    poblacion = [float(P0)]
    for _ in range(len(tiempo) - 1):
        P_t = poblacion[-1]
        poblacion.append(P_t + r * P_t)
    return tiempo, np.array(poblacion)


def modelo_estocastico(P0, r, sigma, tiempo, seed=None):
    """Modelo estocástico: P_{t+1} = P_t + r * P_t + eps_t, eps_t ~ N(0, sigma^2).

    Si la nueva población resulta negativa, se fija en 0.

    Parámetros:
        P0 (float): población inicial.
        r (float): tasa de crecimiento.
        sigma (float): desviación estándar del ruido normal.
        tiempo (array_like): vector de períodos (0 a T).
        seed (int or None): semilla para np.random.default_rng (reproducibilidad).

    Retorna:
        tuple: (tiempo, poblacion) como arreglos numpy.
    """
    tiempo = np.asarray(tiempo, dtype=float)
    rng = np.random.default_rng(seed)
    poblacion = [float(P0)]
    for _ in range(len(tiempo) - 1):
        P_t = poblacion[-1]
        eps_t = rng.normal(loc=0.0, scale=sigma)
        P_nuevo = P_t + r * P_t + eps_t
        if P_nuevo < 0:
            P_nuevo = 0.0
        poblacion.append(P_nuevo)
    return tiempo, np.array(poblacion)


def modelo_continuo_euler(P0, r, tiempo, dt):
    """Modelo continuo (Euler): P_{t+dt} = P_t + dt * (r * P_t).

    El vector de tiempo se construye con el tamaño de paso dt,
    desde tiempo[0] hasta tiempo[-1].

    Parámetros:
        P0 (float): población inicial.
        r (float): tasa de crecimiento.
        tiempo (array_like): vector de tiempo de referencia (de 0 a T).
        dt (float): tamaño de paso (> 0).

    Retorna:
        tuple: (tiempo, poblacion) como arreglos numpy.
    """
    if dt <= 0:
        raise ValueError("dt debe ser positivo.")
    # Vector de tiempo construido con dt (incluye el extremo final)
    t = np.arange(tiempo[0], tiempo[-1] + dt / 2, dt)
    poblacion = np.empty_like(t)
    poblacion[0] = P0
    for i in range(1, len(t)):
        P_anterior = poblacion[i - 1]
        poblacion[i] = P_anterior + dt * (r * P_anterior)
    return t, poblacion


if __name__ == "__main__":
    # Verificación rápida (sin simulaciones largas)
    r = estimar_r(datos)
    t0 = np.arange(0, T_DEFECTO + 1)
    print(f"r estimado = {r:.6f}")
    for nombre, (t, p) in {
        "determinístico": modelo_deterministico(P0_DEFECTO, r, t0),
        "discreto": modelo_discreto(P0_DEFECTO, r, t0),
        "estocástico": modelo_estocastico(P0_DEFECTO, r, SIGMA_DEFECTO, t0, seed=42),
        "continuo (Euler)": modelo_continuo_euler(P0_DEFECTO, r, t0, DT_DEFECTO),
    }.items():
        print(f"{nombre:>16}: {len(t)} puntos, P_final = {p[-1]:.2f}")
