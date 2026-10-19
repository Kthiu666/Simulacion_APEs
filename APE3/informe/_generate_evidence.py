"""Genera tabla y graficas para el informe de la Practica 03.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from controller import simulation_controller as controller

IMG = os.path.join(HERE, "img")
os.makedirs(IMG, exist_ok=True)

NUM_CUSTOMERS = 10000
SEED = 42

results = controller.run_all_scenarios(NUM_CUSTOMERS, SEED)
rows = controller.build_comparison_rows(results)

with open(os.path.join(HERE, "resultados.json"), "w", encoding="utf-8") as fh:
    json.dump(rows, fh, ensure_ascii=False, indent=2)

colors = {"1": "#2563eb", "2": "#f59e0b", "3": "#dc2626"}

for result in results:
    scenario = result["scenario"]
    theoretical = result["theoretical"]
    simulation = result["simulation"]
    sid = scenario["id"]
    label = f"lambda={scenario['lambda_rate']}, mu={scenario['mu_rate']}"

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.step(
        simulation.queue_series_times,
        simulation.queue_series_lengths,
        where="post",
        color=colors[sid],
        linewidth=0.9,
        label="Tamano de la cola (simulado)",
    )
    ax.axhline(
        theoretical.Lq,
        color="#111827",
        linestyle="--",
        linewidth=1.4,
        label=f"Lq teorica = {theoretical.Lq:.3f}",
    )
    ax.set_title(f"Escenario {sid} ({label}): evolucion del tamano de la cola")
    ax.set_xlabel("Tiempo (unidades de tiempo)")
    ax.set_ylabel("Clientes esperando")
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, f"cola_escenario_{sid}.png"), dpi=130)
    plt.close(fig)

    waiting = [record.waiting_time for record in simulation.customers]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.hist(waiting, bins=40, color=colors[sid], edgecolor="white")
    ax.axvline(
        theoretical.Wq,
        color="#111827",
        linestyle="--",
        linewidth=1.4,
        label=f"Wq teorica = {theoretical.Wq:.3f}",
    )
    ax.axvline(
        simulation.avg_waiting_time,
        color="#b91c1c",
        linestyle="-",
        linewidth=1.4,
        label=f"Wq simulada = {simulation.avg_waiting_time:.3f}",
    )
    ax.set_title(f"Escenario {sid} ({label}): distribucion de tiempos de espera")
    ax.set_xlabel("Tiempo de espera en la cola (unidades de tiempo)")
    ax.set_ylabel("Cantidad de clientes")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, f"espera_escenario_{sid}.png"), dpi=130)
    plt.close(fig)

labels = [f"Esc. {row['Escenario'][-1]}" for row in rows]

for key_theo, key_sim, title, ylabel, name in [
    ("Wq te\u00f3rica (t. espera)", "Wq simulada (t. espera)", "Comparacion de Wq (tiempo de espera)", "Tiempo (unidades)", "comparacion_wq.png"),
    ("Lq te\u00f3rica", "Lq simulada (cola)", "Comparacion de Lq (tamano de cola)", "Clientes", "comparacion_lq.png"),
]:
    theo = [row[key_theo] for row in rows]
    sim = [row[key_sim] for row in rows]
    positions = np.arange(len(labels))
    width = 0.38
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(positions - width / 2, theo, width, label="Teorica", color="#94a3b8")
    ax.bar(positions + width / 2, sim, width, label="Simulada", color="#2563eb")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, name), dpi=130)
    plt.close(fig)

print(json.dumps(rows, ensure_ascii=False, indent=2))
