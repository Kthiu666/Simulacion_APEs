"""Configuración global y tablas de clasificación."""

RAIN_CLASSIFICATION_TABLE = [
    (0.00, 0.40, "Sin lluvia"),
    (0.40, 0.60, "Baja posibilidad"),
    (0.60, 0.75, "Lluvia probable"),
    (0.75, 1.01, "Lluvia")
]

TEMPERATURE_TABLE = {
    10: 1.00,
    12: 0.90,
    14: 0.80,
    16: 0.70,
    18: 0.60,
    20: 0.50,
    22: 0.40,
    24: 0.30,
    26: 0.20,
    28: 0.10
}