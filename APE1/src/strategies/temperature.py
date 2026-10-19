from src.domain.interfaces import ITemperatureStrategy

class LinearInterpolationTemperatureStrategy(ITemperatureStrategy):
    """
    Calcula Tf mediante interpolación lineal continua:
    Tf(T) = 1.50 - 0.05 * T (para 10 <= T <= 28)
    """
    def calculate_tf(self, temp: float) -> float:
        if temp <= 10.0:
            return 1.00
        elif temp >= 28.0:
            return 0.10
        return round(1.50 - 0.05 * temp, 4)