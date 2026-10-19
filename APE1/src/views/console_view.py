from typing import List
from src.domain.entities import SimulationResult

class ConsolePresenter:
    @staticmethod
    def display_results_table(title: str, results: List[SimulationResult]):
        print("\n" + "="*85)
        print(f" {title.upper()} ")
        print("="*85)
        header = f"{'Hora':<7} | {'Hum(%)':<6} | {'Nub(%)':<6} | {'Temp(°C)':<8} | {'H':<5} | {'N':<5} | {'Tf':<5} | {'Índice':<7} | {'Estado':<16}"
        print(header)
        print("-" * 85)
        
        for r in results:
            row = (
                f"{r.data.hour:<7} | "
                f"{r.data.humidity_pct:<6.0f} | "
                f"{r.data.cloudiness_pct:<6.0f} | "
                f"{r.data.temperature_c:<8.0f} | "
                f"{r.data.H:<5.2f} | "
                f"{r.data.N:<5.2f} | "
                f"{r.tf:<5.2f} | "
                f"{r.index:<7.4f} | "
                f"{r.category:<16}"
            )
            print(row)
        print("="*85)