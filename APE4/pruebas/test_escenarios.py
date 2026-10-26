"""Escenarios y validación del intercambio con configuraciones variables."""
import csv
import io
from contextlib import redirect_stdout
from unittest.mock import patch
import main as entrada
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from config import ESCENARIOS, ParametrosSIR
from main import crear_argumentos, resolver_parametros
from comparar import cargar_comparacion
from resultados.exportador import exportar_csv, exportar_parametros
from resultados.lectura import leer_parametros, leer_serie
from simulacion.motor import ejecutar


class TestEscenarios(unittest.TestCase):
    def test_normal_conserva_guia(self):
        self.assertEqual(ESCENARIOS['normal'], ParametrosSIR())
        self.assertEqual(resolver_parametros(crear_argumentos([])), ParametrosSIR())

    def test_perfiles_solo_cambian_beta_gamma(self):
        normal = ESCENARIOS['normal']
        for p in ESCENARIOS.values():
            self.assertEqual(replace(p, beta=normal.beta, gamma=normal.gamma), normal)
        self.assertGreater(ESCENARIOS['malo'].beta, normal.beta)
        self.assertLess(ESCENARIOS['malo'].gamma, normal.gamma)
        self.assertLess(ESCENARIOS['favorable'].beta, normal.beta)
        self.assertGreater(ESCENARIOS['favorable'].gamma, normal.gamma)

    def test_argumentos_sustituyen_perfil_incluso_cero(self):
        args = crear_argumentos(['--escenario','malo','--beta','0','--infectados','0',
                                '--pasos','0','--semilla','-7'])
        self.assertEqual(resolver_parametros(args), ParametrosSIR(
            beta=0, gamma=0.05, infectados_iniciales=0, pasos=0, semilla=-7))

    def test_valores_personalizados_y_contactos(self):
        p = resolver_parametros(crear_argumentos(['--poblacion','200','--infectados','10',
            '--beta','0.2','--gamma','0.15','--pasos','150','--contactos','2','--semilla','7']))
        r = ejecutar(p)
        self.assertEqual(len(r.registros), 151)
        self.assertEqual(r.registros[0].susceptibles, 190)
        r.validar()

    def test_semilla_compatible_netlogo(self):
        for semilla in (-2147483648, 2147483647):
            ParametrosSIR(semilla=semilla)
        for semilla in (-2147483649, 2147483648):
            with self.assertRaises(ValueError):
                ParametrosSIR(semilla=semilla)

    def test_probabilidades_numericas_finitas(self):
        for valor in (True, '0.5', None, float('inf'), float('nan')):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                ParametrosSIR(beta=valor)


class TestIntercambio(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.carpeta = Path(self.temp.name)

    def guardar(self, p, origen='python'):
        r = ejecutar(p)
        exportar_csv(r, self.carpeta/f'resultados_{origen}.csv')
        exportar_parametros(r, self.carpeta/f'parametros_{origen}.csv')
        return r

    def test_ida_vuelta_variable(self):
        p = ParametrosSIR(poblacion=40, infectados_iniciales=3, pasos=12,
                          contactos_por_infectado=3, semilla=-2)
        r = self.guardar(p)
        self.assertEqual(leer_parametros(self.carpeta/'parametros_python.csv'), p)
        filas = leer_serie(self.carpeta/'resultados_python.csv')
        self.assertEqual(len(filas), 13)
        self.assertEqual(filas[-1], [12, r.registros[-1].susceptibles,
                                    r.registros[-1].infectados, r.registros[-1].recuperados])

    def test_cero_pasos_y_cero_infectados(self):
        self.guardar(ParametrosSIR(poblacion=2, infectados_iniciales=0, pasos=0))
        self.assertEqual(leer_serie(self.carpeta/'resultados_python.csv'), [[0, 2, 0, 0]])

    def test_metadatos_obligatorios(self):
        exportar_csv(ejecutar(ParametrosSIR()), self.carpeta/'resultados_python.csv')
        with self.assertRaises(FileNotFoundError):
            leer_serie(self.carpeta/'resultados_python.csv')

    def test_rechaza_beta_distinta_aunque_coincida_condicion_inicial(self):
        self.guardar(ParametrosSIR(), 'python')
        self.guardar(ParametrosSIR(beta=0.6), 'netlogo')
        with self.assertRaisesRegex(ValueError, 'parámetros distintos'):
            cargar_comparacion(self.carpeta)

    def test_comparacion_variable_valida(self):
        p = ParametrosSIR(poblacion=20, infectados_iniciales=2, pasos=5)
        self.guardar(p, 'python'); self.guardar(p, 'netlogo')
        cfg, a, b = cargar_comparacion(self.carpeta)
        self.assertEqual(cfg, p)
        self.assertEqual(a, b)

    def test_rechaza_tiempo_suma_y_columnas_incorrectas(self):
        p = ParametrosSIR(pasos=1)
        for ultima in ([2,94,6,0], [1,94,7,0], [1,94,6], [1,94,6,0,0], [1,94.5,5.5,0]):
            with self.subTest(ultima=ultima):
                self.guardar(p)
                ruta = self.carpeta/'resultados_python.csv'
                with ruta.open('w', newline='') as f:
                    csv.writer(f).writerows([['tiempo','susceptibles','infectados','recuperados'],
                                             [0,95,5,0], ultima])
                with self.assertRaises(ValueError):
                    leer_serie(ruta)

    def test_perfil_no_sobrescribe_caso_base(self):
        base = self.carpeta / 'netlogo/resultados_python.csv'
        base.parent.mkdir()
        base.write_text('corrida base conservada')
        args = crear_argumentos(['--escenario', 'malo'])
        with patch.object(entrada, 'RAIZ', self.carpeta), patch.object(entrada, 'crear_argumentos', return_value=args), \
             patch.object(entrada, 'guardar_grafica', return_value=self.carpeta/'grafica.png'), redirect_stdout(io.StringIO()):
            self.assertEqual(entrada.main(), 0)
        self.assertEqual(base.read_text(), 'corrida base conservada')
        self.assertEqual(leer_parametros(self.carpeta/'netlogo/escenarios/malo/parametros_python.csv'), ESCENARIOS['malo'])

    def test_variacion_de_perfil_se_guarda_como_personalizado(self):
        args = crear_argumentos(['--escenario', 'favorable', '--beta', '0'])
        with patch.object(entrada, 'RAIZ', self.carpeta), patch.object(entrada, 'crear_argumentos', return_value=args), \
             patch.object(entrada, 'guardar_grafica', return_value=self.carpeta/'grafica.png'), redirect_stdout(io.StringIO()):
            self.assertEqual(entrada.main(), 0)
        self.assertEqual(leer_parametros(self.carpeta/'netlogo/parametros_python.csv'),
                         replace(ESCENARIOS['favorable'], beta=0))
        self.assertFalse((self.carpeta/'netlogo/escenarios/favorable').exists())

    def test_rechaza_parametros_incompletos(self):
        self.guardar(ParametrosSIR())
        ruta = self.carpeta/'parametros_python.csv'
        ruta.write_text('poblacion,beta\n100,0.3\n')
        with self.assertRaises(ValueError):
            leer_parametros(ruta)


if __name__ == '__main__':
    unittest.main()
