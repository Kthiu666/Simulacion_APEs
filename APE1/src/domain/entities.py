from dataclasses import dataclass

@dataclass
class WeatherData:
    hour: str
    humidity_pct: float       # Humedad en % (0 - 100)
    cloudiness_pct: float     # Nubosidad en % (0 - 100)
    temperature_c: float      # Temperatura en °C

    @property
    def H(self) -> float:
        return self.humidity_pct / 100.0

    @property
    def N(self) -> float:
        return self.cloudiness_pct / 100.0

@dataclass
class SimulationResult:
    data: WeatherData
    tf: float
    index: float
    category: str