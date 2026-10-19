"""Comparación de los 4 modelos de crecimiento poblacional (Práctica 02).

Ejecuta los modelos determinístico, discreto, estocástico y continuo (Euler)
con los parámetros de la guía, los grafica junto con los datos reales,
guarda los resultados en resultados/comparacion.csv e imprime una tabla
con las poblaciones finales y los errores.

Uso:
    python comparacion.py              # guarda PNG en resultados/
    python comparacion.py --mostrar    # además muestra la figura con plt.show()
"""

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from modelos import (P0_DEFECTO, datos, estimar_r, modelo_continuo_euler,
                     modelo_deterministico, modelo_discreto,
                     modelo_estocastico)

# Parámetros de la comparación
P0 = datos[0]             # población inicial = 1000
r = estimar_r(datos)      # r = ln(2100/1000)/6 ≈ 0.123656
sigma = 30                # desviación estándar del ruido
dt = 0.1                  # tamaño de paso del modelo continuo
TIEMPO = 6                # períodos (len(datos) - 1)
SEED = 42                 # semilla fija para reproducibilidad
N_PUNTOS = 100            # puntos del modelo determinístico
DIR_RESULTADOS = "resultados"


def main(mostrar=False):
    """Ejecuta los 4 modelos, guarda CSV/PNG e imprime la tabla de errores.

    Parámetros:
        mostrar (bool): si es True, muestra la figura con plt.show().
    """
    # Tiempo de referencia: 0 a 6 períodos
    tiempo = np.arange(0, TIEMPO + 1)

    # Ejecutar los 4 modelos
    t_det, p_det = modelo_deterministico(P0, r, tiempo, n_puntos=N_PUNTOS)
    t_dis, p_dis = modelo_discreto(P0, r, tiempo)
    t_est, p_est = modelo_estocastico(P0, r, sigma, tiempo, seed=SEED)
    t_eul, p_eul = modelo_continuo_euler(P0, r, tiempo, dt)

    modelos = [("deterministico", t_det, p_det),
               ("discreto", t_dis, p_dis),
               ("estocastico", t_est, p_est),
               ("euler", t_eul, p_eul)]

    # Guardar resultados en CSV
    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    ruta_csv = os.path.join(DIR_RESULTADOS, "comparacion.csv")
    with open(ruta_csv, "w", encoding="utf-8") as archivo:
        archivo.write("modelo,tiempo,poblacion\n")
        for nombre, t, p in modelos:
            for ti, pi in zip(t, p):
                archivo.write(f"{nombre},{ti:.4f},{pi:.4f}\n")
    print(f"Resultados guardados en {ruta_csv}")

    # Gráfica comparativa (título, ejes, leyenda, cuadrícula + datos reales)
    plt.figure(figsize=(9, 5))
    plt.plot(t_det, p_det, label="Determinístico", linewidth=2)
    plt.plot(t_dis, p_dis, marker="o", label="Discreto")
    plt.plot(t_est, p_est, marker="s", label="Estocástico")
    plt.plot(t_eul, p_eul, label="Continuo (Euler)")
    plt.plot(tiempo, datos, "k*", markersize=12, label="Datos reales")

    plt.title("Comparación de modelos de crecimiento poblacional")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    ruta_png = os.path.join(DIR_RESULTADOS, "comparacion.png")
    plt.tight_layout()
    plt.savefig(ruta_png, dpi=150)
    print(f"Gráfica guardada en {ruta_png}")
    if mostrar:
        plt.show()
    else:
        plt.close()

    # Tabla de poblaciones finales y errores
    P_det_final = p_det[-1]          # referencia: modelo determinístico
    dato_real_final = datos[-1]      # último dato real = 2100
    print()
    print(f"{'Modelo':<16} {'P final':>10} {'|err det.|':>12} {'|err real|':>12}")
    print("-" * 52)
    for nombre, _, p in modelos:
        p_final = p[-1]
        err_det = abs(p_final - P_det_final)
        err_real = abs(p_final - dato_real_final)
        print(f"{nombre:<16} {p_final:>10.2f} {err_det:>12.2f} {err_real:>12.2f}")
    print("-" * 52)
    print(f"{'referencia':<16} {P_det_final:>10.2f} {'-':>12} "
          f"{abs(P_det_final - dato_real_final):>12.2f}  (determinístico vs dato real)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compara los 4 modelos de crecimiento poblacional.")
    parser.add_argument("--mostrar", action="store_true",
                        help="muestra la figura con plt.show()")
    args = parser.parse_args()
    main(mostrar=args.mostrar)
