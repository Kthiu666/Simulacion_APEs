from typing import List
from src.domain.entities import WeatherData, SimulationResult
from src.domain.interfaces import ITemperatureStrategy, IRainModelStrategy
from config.settings import RAIN_CLASSIFICATION_TABLE

class RainSimulatorService:
    def __init__(self, temp_strategy: ITemperatureStrategy, model_strategy: IRainModelStrategy):
        self.temp_strategy = temp_strategy
        self.model_strategy = model_strategy

    def _classify_index(self, index: float) -> str:
        for min_val, max_val, category in RAIN_CLASSIFICATION_TABLE:
            if min_val <= index < max_val:
                return category
        if index >= 0.75:
            return "Lluvia"
        return "Sin lluvia"

    def run_simulation(self, weather_dataset: List[WeatherData]) -> List[SimulationResult]:
        results = []
        for data in weather_dataset:
            tf = self.temp_strategy.calculate_tf(data.temperature_c)
            idx = self.model_strategy.calculate_index(data, tf)
            cat = self._classify_index(idx)
            results.append(SimulationResult(data=data, tf=tf, index=idx, category=cat))
        return results