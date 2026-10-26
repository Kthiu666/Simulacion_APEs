#!/usr/bin/env python3
"""Genera tres casos SIR y sus archivos Python para cargarlos directamente en NetLogo."""
import csv
from pathlib import Path

from config import ESCENARIOS
from simulacion.motor import ejecutar
from resultados.exportador import exportar_csv, exportar_parametros
from resultados.graficas import guardar_grafica

RAIZ = Path(__file__).resolve().parent


def generar() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True, constrained_layout=True)
    resumen = []
    for (nombre, p), color in zip(ESCENARIOS.items(), ("#D14A46", "#2276BA", "#279A68")):
        resultado = ejecutar(p)
        carpeta = RAIZ / "netlogo/escenarios" / nombre
        exportar_csv(resultado, carpeta / "resultados_python.csv")
        exportar_parametros(resultado, carpeta / "parametros_python.csv")
        guardar_grafica(resultado, RAIZ / "graficas/escenarios" / nombre)
        registros = resultado.registros
        pico = max(registros, key=lambda r: r.infectados)
        final = registros[-1]
        resumen.append([nombre, p.beta, p.gamma, pico.infectados, pico.tiempo,
                        final.susceptibles, final.infectados, final.recuperados,
                        p.poblacion - final.susceptibles])
        for ax, campo in zip(axes, ("susceptibles", "infectados", "recuperados")):
            ax.plot([r.tiempo for r in registros], [getattr(r, campo) for r in registros],
                    color=color, linewidth=2, label=nombre.capitalize())
    for ax, titulo in zip(axes, ("Susceptibles", "Infectados", "Recuperados")):
        ax.set(title=titulo, ylabel="Personas", xlim=(0, 100), ylim=(0, 100))
        ax.grid(alpha=0.2)
        ax.legend()
    axes[-1].set_xlabel("Tiempo (pasos); semilla 42 en cada caso")
    salida = RAIZ / "graficas/escenarios"
    salida.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida / "comparacion_escenarios.png", dpi=170)
    plt.close(fig)
    with (salida / "resumen_escenarios.csv").open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["escenario", "beta", "gamma", "pico_infectados", "tiempo_pico",
                           "susceptibles_finales", "infectados_finales", "recuperados_finales",
                           "personas_infectadas_acumuladas"])
        escritor.writerows(resumen)
    for fila in resumen:
        print(f"{fila[0]:10} beta={fila[1]:.2f} gamma={fila[2]:.2f} "
              f"pico I={fila[3]} en t={fila[4]}, final (S,I,R)={tuple(fila[5:8])}")
    print(f"Gráfica de los tres casos: {salida / 'comparacion_escenarios.png'}")
    print("Son escenarios ilustrativos; favorable no implica un óptimo matemático ni garantiza una trayectoria concreta.")


if __name__ == "__main__":
    generar()
