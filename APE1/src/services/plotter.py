from typing import List
import matplotlib.pyplot as plt
from src.domain.entities import SimulationResult

class WeatherPlotterService:
    @staticmethod
    def plot_comparison(results_base: List[SimulationResult], results_adj: List[SimulationResult], output_filename="simulacion_lluvia.png"):
        hours = [r.data.hour for r in results_base]
        indices_base = [r.index for r in results_base]
        indices_adj = [r.index for r in results_adj]
        temps = [r.data.temperature_c for r in results_base]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # Gráfica 1: Comparación de Índices de Lluvia
        ax1.plot(hours, indices_base, marker='o', color='blue', linewidth=2, label='Modelo Base')
        ax1.plot(hours, indices_adj, marker='s', color='green', linewidth=2, linestyle='--', label='Modelo Ajustado')
        ax1.axhline(y=0.75, color='red', linestyle=':', label='Umbral Lluvia (>0.75)')
        ax1.axhline(y=0.60, color='orange', linestyle=':', label='Umbral Lluvia Probable (>0.60)')
        ax1.set_ylabel('Índice de Lluvia (I)')
        ax1.set_title('Simulación Meteorológica: Comportamiento del Índice de Lluvia')
        ax1.grid(True, linestyle='--', alpha=0.6)
        ax1.legend(loc='upper right')

        # Gráfica 2: Comportamiento de Temperatura y Tf
        tfs = [r.tf for r in results_base]
        ax2.plot(hours, temps, marker='^', color='red', label='Temperatura (°C)')
        ax2.plot(hours, tfs, marker='d', color='purple', label='Factor Temp (Tf)')
        ax2.set_xlabel('Hora del Día')
        ax2.set_ylabel('Valor')
        ax2.set_title('Evolución de Temperatura y Factor Tf')
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.legend(loc='upper right')

        plt.tight_layout()
        plt.savefig(output_filename)
        plt.close()
        print(f"\n[INFO] Gráfica guardada exitosamente como '{output_filename}'")