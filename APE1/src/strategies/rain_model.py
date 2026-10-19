from src.domain.interfaces import IRainModelStrategy
from src.domain.entities import WeatherData

class BaseRainModelStrategy(IRainModelStrategy):
    """Modelo Original: I = 0.5*H + 0.3*N + 0.2*Tf"""
    def calculate_index(self, data: WeatherData, tf: float) -> float:
        i = 0.5 * data.H + 0.3 * data.N + 0.2 * tf
        return round(i, 4)

    def get_model_name(self) -> str:
        return "Modelo Base (Lineal)"


class AdjustedRainModelStrategy(IRainModelStrategy):
    """Modelo Ajustado Sinérgico: I = 0.4*H + 0.4*N + 0.2*Tf + 0.1*(H*N)"""
    def calculate_index(self, data: WeatherData, tf: float) -> float:
        i = 0.4 * data.H + 0.4 * data.N + 0.2 * tf + 0.1 * (data.H * data.N)
        return round(i, 4)

    def get_model_name(self) -> str:
        return "Modelo Ajustado (Sinérgico H*N)"