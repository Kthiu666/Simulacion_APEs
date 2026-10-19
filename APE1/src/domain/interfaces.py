from abc import ABC, abstractmethod
from src.domain.entities import WeatherData

class ITemperatureStrategy(ABC):
    @abstractmethod
    def calculate_tf(self, temp: float) -> float:
        pass

class IRainModelStrategy(ABC):
    @abstractmethod
    def calculate_index(self, data: WeatherData, tf: float) -> float:
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        pass