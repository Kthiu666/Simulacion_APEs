"""Experimentos de sensibilidad (Práctica 02 - Simulación).

Genera en resultados/:
  1) influencia_r.png         -> determinístico y discreto con
                                 r en {-0.05, 0.05, r_estimado, 0.25}
  2) influencia_sigma.png     -> estocástico con sigma en {0, 10, 30, 80},
                                 30 corridas c/u (bandas p5-p95 y media)
  3) influencia_dt.png        -> Euler con dt en {1, 0.5, 0.1, 0.01}
                                 contra la solución exacta (imprime errores)
  4) discreto_vs_continuo.png -> comparación directa
  5) nuevos_datos.png         -> pipeline completo con otro arreglo (decrecimiento)

Además guarda un resumen numérico en resultados/resumen.csv.
Semilla fija (SEED = 42) para reproducibilidad.

Uso:
    python experimentos.py              # guarda los PNG y resumen.csv
    python experimentos.py --mostrar    # además muestra las figuras
"""

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from modelos import (datos, estimar_r, modelo_continuo_euler,
                     modelo_deterministico, modelo_discreto,
                     modelo_estocastico)

# Parámetros de la práctica
P0 = datos[0]                    # 1000
r = estimar_r(datos)             # ln(2100/1000)/6 ≈ 0.123656
T = len(datos) - 1               # 6 períodos
SEED = 42                        # semilla fija
N_CORRIDAS = 30                  # corridas por cada sigma
DT_COMPARACION = 0.1             # dt del modelo Euler "de la práctica"
DIR_RESULTADOS = "resultados"

# Filas para resumen.csv: (experimento, modelo, parametro, p_final, error)
filas_resumen = []


def agregar_fila(experimento, modelo, parametro, p_final, error=""):
    """Agrega una fila al resumen numérico."""
    filas_resumen.append((experimento, modelo, parametro, p_final, error))


def experimento_influencia_r(mostrar=False):
    """1) Determinístico y discreto con r en {-0.05, 0.05, r_estimado, 0.25}."""
    valores_r = [-0.05, 0.05, r, 0.25]
    tiempo_fino = np.linspace(0, T, 200)
    tiempo_pasos = np.arange(0, T + 1)

    plt.figure(figsize=(9, 5))
    for r_val in valores_r:
        # Modelo determinístico (curva continua)
        t_det, p_det = modelo_deterministico(P0, r_val, tiempo_fino)
        etiqueta_r = f"r = {r_val:+.3f}"
        plt.plot(t_det, p_det, "-", label=f"Det {etiqueta_r}")

        # Modelo discreto (períodos)
        t_dis, p_dis = modelo_discreto(P0, r_val, tiempo_pasos)
        plt.plot(t_dis, p_dis, "o--", markersize=4,
                 label=f"Disc {etiqueta_r}")

        error = abs(p_dis[-1] - p_det[-1])
        agregar_fila("influencia_r", "deterministico", etiqueta_r,
                     p_det[-1], 0.0)
        agregar_fila("influencia_r", "discreto", etiqueta_r,
                     p_dis[-1], error)

    plt.title("Influencia de r: modelos determinístico y discreto")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.legend(fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)

    ruta = os.path.join(DIR_RESULTADOS, "influencia_r.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    if mostrar:
        plt.show()
    else:
        plt.close()
    print(f"Guardada en {ruta}")


def experimento_influencia_sigma(mostrar=False):
    """2) Estocástico con sigma en {0, 10, 30, 80}: 30 corridas, media y p5-p95."""
    valores_sigma = [0, 10, 30, 80]
    tiempo = np.arange(0, T + 1)
    rng = np.random.default_rng(SEED)
    # Semillas reproducibles e independientes para cada corrida
    semillas = rng.integers(0, 2**31, size=N_CORRIDAS)

    # Referencia determinística
    t_det, p_det = modelo_deterministico(P0, r, tiempo)

    plt.figure(figsize=(9, 5))
    plt.plot(t_det, p_det, "k--", linewidth=2,
             label="Determinístico (referencia)")

    for sigma in valores_sigma:
        # 30 corridas del modelo estocástico
        corridas = np.array([
            modelo_estocastico(P0, r, sigma, tiempo, seed=int(s))[1]
            for s in semillas
        ])
        media = corridas.mean(axis=0)
        p5, p95 = np.percentile(corridas, [5, 95], axis=0)

        # Banda de percentiles 5-95 y media
        plt.fill_between(tiempo, p5, p95, alpha=0.20,
                         label=f"sigma = {sigma} (p5-p95)")
        plt.plot(tiempo, media, linewidth=1.8,
                 label=f"sigma = {sigma} (media)")

        agregar_fila("influencia_sigma", "estocastico",
                     f"sigma={sigma} (media)", media[-1],
                     abs(media[-1] - p_det[-1]))
        agregar_fila("influencia_sigma", "estocastico",
                     f"sigma={sigma} (p5)", p5[-1])
        agregar_fila("influencia_sigma", "estocastico",
                     f"sigma={sigma} (p95)", p95[-1])

    plt.plot(tiempo, datos, "k*", markersize=12, label="Datos reales")
    plt.title(f"Influencia de sigma: {N_CORRIDAS} corridas por valor (semilla {SEED})")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.legend(fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)

    ruta = os.path.join(DIR_RESULTADOS, "influencia_sigma.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    if mostrar:
        plt.show()
    else:
        plt.close()
    print(f"Guardada en {ruta}")


def experimento_influencia_dt(mostrar=False):
    """3) Euler con dt en {1, 0.5, 0.1, 0.01} contra la solución exacta."""
    valores_dt = [1.0, 0.5, 0.1, 0.01]
    tiempo = np.arange(0, T + 1)

    # Solución exacta P(t) = P0 * e^(r t)
    t_det, p_det = modelo_deterministico(P0, r, tiempo)
    exacto_final = P0 * np.exp(r * T)

    plt.figure(figsize=(9, 5))
    plt.plot(t_det, p_det, "k--", linewidth=2,
             label="Solución exacta (referencia)")

    print("\nError final de Euler vs solución exacta (t = 6):")
    for dt in valores_dt:
        t_eul, p_eul = modelo_continuo_euler(P0, r, tiempo, dt)
        error = abs(p_eul[-1] - exacto_final)
        plt.plot(t_eul, p_eul, marker=".", markersize=4,
                 label=f"dt = {dt}")
        agregar_fila("influencia_dt", "euler", f"dt={dt}", p_eul[-1], error)
        print(f"  dt = {dt:<5}: P_final = {p_eul[-1]:9.2f}  error = {error:9.4f}")

    plt.title("Influencia de dt: método de Euler vs solución exacta")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    ruta = os.path.join(DIR_RESULTADOS, "influencia_dt.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    if mostrar:
        plt.show()
    else:
        plt.close()
    print(f"Guardada en {ruta}")


def experimento_discreto_vs_continuo(mostrar=False):
    """4) Comparación directa del modelo discreto contra el continuo (Euler)."""
    tiempo = np.arange(0, T + 1)
    exacto_final = P0 * np.exp(r * T)

    t_dis, p_dis = modelo_discreto(P0, r, tiempo)
    t_eul, p_eul = modelo_continuo_euler(P0, r, tiempo, DT_COMPARACION)
    t_det, p_det = modelo_deterministico(P0, r, tiempo)

    plt.figure(figsize=(9, 5))
    plt.plot(t_det, p_det, "k--", linewidth=2, label="Determinístico (exacto)")
    plt.plot(t_dis, p_dis, "o-", label="Discreto (períodos)")
    plt.plot(t_eul, p_eul, label=f"Continuo (Euler, dt = {DT_COMPARACION})")
    plt.plot(tiempo, datos, "k*", markersize=12, label="Datos reales")

    plt.title("Discreto vs continuo: comparación directa")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    agregar_fila("discreto_vs_continuo", "discreto", f"r={r:.4f}",
                 p_dis[-1], abs(p_dis[-1] - exacto_final))
    agregar_fila("discreto_vs_continuo", "euler", f"dt={DT_COMPARACION}",
                 p_eul[-1], abs(p_eul[-1] - exacto_final))

    ruta = os.path.join(DIR_RESULTADOS, "discreto_vs_continuo.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    if mostrar:
        plt.show()
    else:
        plt.close()
    print(f"Guardada en {ruta}")


def experimento_nuevos_datos(mostrar=False):
    """5) Pipeline completo con otro arreglo (decrecimiento), re-estimando r."""
    nuevos = [500, 450, 400, 380, 340, 300, 280]
    P0_nuevo = nuevos[0]
    r_nuevo = estimar_r(nuevos)          # ln(280/500)/6 < 0 -> decrecimiento
    T_nuevo = len(nuevos) - 1
    tiempo = np.arange(0, T_nuevo + 1)

    t_det, p_det = modelo_deterministico(P0_nuevo, r_nuevo, tiempo)
    t_dis, p_dis = modelo_discreto(P0_nuevo, r_nuevo, tiempo)
    t_est, p_est = modelo_estocastico(P0_nuevo, r_nuevo, 30, tiempo, seed=SEED)
    t_eul, p_eul = modelo_continuo_euler(P0_nuevo, r_nuevo, tiempo,
                                         DT_COMPARACION)

    plt.figure(figsize=(9, 5))
    plt.plot(t_det, p_det, label="Determinístico", linewidth=2)
    plt.plot(t_dis, p_dis, marker="o", label="Discreto")
    plt.plot(t_est, p_est, marker="s", label="Estocástico (sigma = 30)")
    plt.plot(t_eul, p_eul, label=f"Continuo (Euler, dt = {DT_COMPARACION})")
    plt.plot(tiempo, nuevos, "k*", markersize=12, label="Datos reales")

    plt.title(f"Pipeline con nuevos datos (decrecimiento, r = {r_nuevo:+.4f})")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    dato_final = nuevos[-1]
    for nombre, t, p in [("deterministico", t_det, p_det),
                         ("discreto", t_dis, p_dis),
                         ("estocastico", t_est, p_est),
                         ("euler", t_eul, p_eul)]:
        agregar_fila("nuevos_datos", nombre, f"r={r_nuevo:.4f}",
                     p[-1], abs(p[-1] - dato_final))

    ruta = os.path.join(DIR_RESULTADOS, "nuevos_datos.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    if mostrar:
        plt.show()
    else:
        plt.close()
    print(f"Guardada en {ruta}")
    print(f"Nuevo r estimado = {r_nuevo:.6f} (decrecimiento)")


def guardar_resumen():
    """Guarda el resumen numérico en resultados/resumen.csv."""
    ruta = os.path.join(DIR_RESULTADOS, "resumen.csv")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("experimento,modelo,parametro,p_final,error_final\n")
        for experimento, modelo, parametro, p_final, error in filas_resumen:
            error_txt = f"{error:.4f}" if error != "" else ""
            archivo.write(f"{experimento},{modelo},{parametro},"
                          f"{p_final:.4f},{error_txt}\n")
    print(f"Resumen numérico guardado en {ruta} "
          f"({len(filas_resumen)} filas)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experimentos de sensibilidad de r, sigma y dt.")
    parser.add_argument("--mostrar", action="store_true",
                        help="muestra las figuras con plt.show()")
    args = parser.parse_args()

    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    experimento_influencia_r(mostrar=args.mostrar)
    experimento_influencia_sigma(mostrar=args.mostrar)
    experimento_influencia_dt(mostrar=args.mostrar)
    experimento_discreto_vs_continuo(mostrar=args.mostrar)
    experimento_nuevos_datos(mostrar=args.mostrar)
    guardar_resumen()
