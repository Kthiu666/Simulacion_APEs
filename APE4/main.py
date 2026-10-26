#!/usr/bin/env python3
"""Entrada de la simulación SIR de la práctica APE 4."""
import argparse
from dataclasses import replace
from pathlib import Path
import sys
import time

from config import ParametrosSIR, ESCENARIOS
from resultados.exportador import exportar_csv, exportar_parametros
from resultados.graficas import guardar_grafica
from simulacion.motor import ejecutar

RAIZ = Path(__file__).resolve().parent


def crear_argumentos(argumentos=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Modelo SIR por agentes con SimPy.")
    parser.add_argument("--escenario", choices=tuple(ESCENARIOS),
                        help="Perfil experimental; los argumentos explícitos sustituyen sus valores.")
    parser.add_argument("--poblacion", type=int)
    parser.add_argument("--infectados", type=int)
    parser.add_argument("--beta", type=float)
    parser.add_argument("--gamma", type=float)
    parser.add_argument("--pasos", type=int)
    parser.add_argument("--contactos", type=int)
    parser.add_argument("--semilla", type=int)
    parser.add_argument("--salida", type=Path,
                        help="Carpeta para resultados_python.csv (por defecto junto al modelo NetLogo).")
    parser.add_argument("--graficas", type=Path,
                        help="Carpeta para sir_evolucion.png.")
    return parser.parse_args(argumentos)


def resolver_parametros(args: argparse.Namespace) -> ParametrosSIR:
    valores = ESCENARIOS[args.escenario] if args.escenario else ParametrosSIR()
    nombres = {"poblacion": "poblacion", "infectados": "infectados_iniciales",
               "beta": "beta", "gamma": "gamma", "pasos": "pasos",
               "contactos": "contactos_por_infectado", "semilla": "semilla"}
    cambios = {destino: getattr(args, origen) for origen, destino in nombres.items()
               if getattr(args, origen) is not None}
    return replace(valores, **cambios)


def main() -> int:
    args = crear_argumentos()
    try:
        parametros = resolver_parametros(args)
        perfil_exacto = args.escenario and parametros == ESCENARIOS[args.escenario]
        salida = args.salida or (RAIZ / "netlogo" / "escenarios" / args.escenario
                                if perfil_exacto else RAIZ / "netlogo")
        graficas = args.graficas or (RAIZ / "graficas" / "escenarios" / args.escenario
                                    if perfil_exacto else RAIZ / "graficas")
        inicio = time.perf_counter()
        resultado = ejecutar(parametros)
        duracion = time.perf_counter() - inicio
        # Verificar las dependencias gráficas antes de exportar el CSV.
        ruta_grafica = guardar_grafica(resultado, graficas)
        ruta_csv = exportar_csv(resultado, salida / "resultados_python.csv")
        ruta_parametros = exportar_parametros(resultado, salida / "parametros_python.csv")
        pico = max(resultado.registros, key=lambda r: r.infectados)
        final = resultado.registros[-1]
        print("MODELO SIR - Python + SimPy")
        print(f"Perfil: {args.escenario or 'normal / personalizado'}")
        print(f"N={parametros.poblacion}, I0={parametros.infectados_iniciales}, "
              f"beta={parametros.beta}, gamma={parametros.gamma}, "
              f"pasos={parametros.pasos}, contactos={parametros.contactos_por_infectado}")
        print(f"Semilla: {parametros.semilla} | Registros: {len(resultado.registros)}")
        print(f"Pico de infectados: {pico.infectados} en t={pico.tiempo}")
        print(f"Final (S, I, R): {final.susceptibles}, {final.infectados}, {final.recuperados}")
        print(f"Tiempo de simulación computacional: {duracion:.4f} s")
        print(f"CSV para NetLogo: {ruta_csv}")
        print(f"Parámetros para NetLogo: {ruta_parametros}")
        print(f"Gráfica: {ruta_grafica}")
        return 0
    except ImportError as exc:
        print(f"ERROR: falta una dependencia ({exc}). "
              "Ejecute: python -m pip install -r requirements.txt", file=sys.stderr)
        return 1
    except (ValueError, RuntimeError, AssertionError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
