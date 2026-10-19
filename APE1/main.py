from src.domain.entities import WeatherData
from src.strategies.temperature import LinearInterpolationTemperatureStrategy
from src.strategies.rain_model import BaseRainModelStrategy, AdjustedRainModelStrategy
from src.services.simulator import RainSimulatorService
from src.services.plotter import WeatherPlotterService
from src.views.console_view import ConsolePresenter

def main():
    # Dataset inicial según la guía de la práctica
    dataset = [
        WeatherData("06:00", 65, 40, 14),
        WeatherData("08:00", 70, 50, 16),
        WeatherData("10:00", 68, 45, 18),
        WeatherData("12:00", 60, 30, 22),
        WeatherData("14:00", 75, 70, 20),
        WeatherData("16:00", 85, 85, 18),
        WeatherData("18:00", 92, 95, 16),
        WeatherData("20:00", 88, 90, 17),
        WeatherData("22:00", 80, 75, 15)
    ]

    temp_strategy = LinearInterpolationTemperatureStrategy()

    # 1. Ejecutar Modelo Base
    base_model = BaseRainModelStrategy()
    simulator_base = RainSimulatorService(temp_strategy, base_model)
    results_base = simulator_base.run_simulation(dataset)
    ConsolePresenter.display_results_table("Resultados: Modelo Base", results_base)

    # 2. Ejecutar Modelo Ajustado
    adj_model = AdjustedRainModelStrategy()
    simulator_adj = RainSimulatorService(temp_strategy, adj_model)
    results_adj = simulator_adj.run_simulation(dataset)
    ConsolePresenter.display_results_table("Resultados: Modelo Ajustado (Sinérgico)", results_adj)

    # 3. Generar Gráficas Comparativas
    WeatherPlotterService.plot_comparison(results_base, results_adj, "grafica_simulacion.png")

if __name__ == "__main__":
    main()