"""Lectura validada de las series SIR y de los parámetros que las acompañan."""
import csv
from pathlib import Path

from config import ParametrosSIR
from resultados.exportador import COLUMNAS_NETLOGO, COLUMNAS_PARAMETROS


def leer_parametros(ruta: Path) -> ParametrosSIR:
    with Path(ruta).open(encoding="utf-8", newline="") as archivo:
        filas = list(csv.reader(archivo))
    if len(filas) != 2 or filas[0] != COLUMNAS_PARAMETROS or len(filas[1]) != 7:
        raise ValueError(f"Archivo de parámetros inválido: {ruta}")
    valores = {nombre: (float(valor) if nombre in ("beta", "gamma") else int(valor))
               for nombre, valor in zip(COLUMNAS_PARAMETROS, filas[1])}
    return ParametrosSIR(**valores)


def leer_serie(ruta: Path, parametros: ParametrosSIR | None = None) -> list[list[int]]:
    ruta = Path(ruta)
    if parametros is None:
        parametros = leer_parametros(ruta.with_name(ruta.name.replace("resultados_", "parametros_")))
    with ruta.open(encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo)
        if next(lector, None) != COLUMNAS_NETLOGO:
            raise ValueError(f"Encabezado incorrecto: {ruta}")
        filas = [[int(valor) for valor in fila] for fila in lector]
    inicial = [0, parametros.susceptibles_iniciales, parametros.infectados_iniciales, 0]
    if len(filas) != parametros.pasos + 1 or filas[0] != inicial:
        raise ValueError(f"Longitud o condición inicial incompatible con los parámetros: {ruta}")
    for t, fila in enumerate(filas):
        if len(fila) != 4 or fila[0] != t or min(fila) < 0 or sum(fila[1:]) != parametros.poblacion:
            raise ValueError(f"Registro inválido en t={t}: {ruta}")
        if t and (fila[1] > filas[t - 1][1] or fila[3] < filas[t - 1][3]):
            raise ValueError(f"Transición SIR inválida en t={t}: {ruta}")
    return filas
