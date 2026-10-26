#!/usr/bin/env python3
"""Compara los CSV reales de Python y NetLogo y genera la evidencia del informe."""
import argparse
from pathlib import Path

from resultados.lectura import leer_serie, leer_parametros

RAIZ = Path(__file__).resolve().parent


def cargar_comparacion(carpeta: Path):
    p = leer_parametros(carpeta / "parametros_python.csv")
    if p != leer_parametros(carpeta / "parametros_netlogo.csv"):
        raise ValueError("Python y NetLogo tienen parámetros distintos; genera ambas corridas con los mismos valores")
    return (p, leer_serie(carpeta / "resultados_python.csv", p),
            leer_serie(carpeta / "resultados_netlogo.csv", p))


def main() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--carpeta", type=Path, default=RAIZ / "netlogo",
                        help="Carpeta que contiene los dos CSV y sus archivos de parámetros.")
    parser.add_argument("--graficas", type=Path, help="Carpeta de la gráfica comparativa.")
    args = parser.parse_args()
    p, python, netlogo = cargar_comparacion(args.carpeta)
    fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True, constrained_layout=True)
    for indice, (ax, nombre) in enumerate(zip(axes, ("Susceptibles", "Infectados", "Recuperados")), 1):
        ax.plot([f[0] for f in python], [f[indice] for f in python], color="#2276BA", label="Python + SimPy", linewidth=2)
        ax.plot([f[0] for f in netlogo], [f[indice] for f in netlogo], color="#D14A46", label="NetLogo", linewidth=2, linestyle="--")
        ax.set(title=nombre, ylabel="Personas", xlim=(0, max(1, p.pasos)), ylim=(0, p.poblacion))
        ax.grid(alpha=0.2)
        ax.legend(loc="best")
    axes[-1].set_xlabel("Tiempo (pasos)")
    carpeta = args.graficas or (RAIZ / "graficas" / "escenarios" / args.carpeta.name
                                if args.carpeta.parent.name == "escenarios" else RAIZ / "graficas")
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / "comparacion_python_netlogo.png"
    fig.savefig(destino, dpi=170)
    plt.close(fig)
    print("Herramienta | Pico I | Paso del pico | S final | I final | R final | Extinción")
    for nombre, filas in (("Python", python), ("NetLogo", netlogo)):
        pico = max(filas, key=lambda f: f[2])
        extincion = next((f[0] for f in filas if f[2] == 0), "No ocurrió")
        print(f"{nombre} | {pico[2]} | {pico[0]} | {filas[-1][1]} | {filas[-1][2]} | {filas[-1][3]} | {extincion}")
    print(f"Gráfica: {destino}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, ImportError) as exc:
        raise SystemExit(f"ERROR: {exc}. Ejecuta Python y exporta la corrida NetLogo antes de comparar.")
