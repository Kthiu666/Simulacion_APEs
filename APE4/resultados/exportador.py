"""Autora: Katheryn Contento. Exportacion CSV para NetLogo."""
import csv
from dataclasses import asdict
from pathlib import Path

from simulacion.motor import ResultadoSIR


COLUMNAS_NETLOGO = ["tiempo", "susceptibles", "infectados", "recuperados"]
COLUMNAS_PARAMETROS = ["poblacion", "infectados_iniciales", "beta", "gamma",
                      "pasos", "contactos_por_infectado", "semilla"]


def exportar_csv(resultado: ResultadoSIR, destino: Path) -> Path:
    """CSV compatible con NetLogo: 4 columnas exactas, sin indice adicional."""
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(COLUMNAS_NETLOGO)
        for r in resultado.registros:
            escritor.writerow([r.tiempo, r.susceptibles, r.infectados, r.recuperados])
    return destino


def exportar_parametros(resultado: ResultadoSIR, destino: Path) -> Path:
    """Acompaña el CSV SIR sin alterar sus cuatro columnas exigidas por la guía."""
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_PARAMETROS)
        escritor.writeheader()
        escritor.writerow(asdict(resultado.parametros))
    return destino

