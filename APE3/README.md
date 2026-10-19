# Simulación de un sistema de líneas de espera M/M/1

Práctica 03 de la asignatura **Simulación** — Carrera de **Computación** — **Universidad Nacional de Loja**.

Aplicación en Python que simula una cola M/M/1 con **SimPy**, calcula las métricas
teóricas del modelo, las compara con las métricas obtenidas por la simulación y
visualiza el comportamiento de la cola y los tiempos de espera mediante una
interfaz web local en **Streamlit**.

> **Grupo 2 — Integrantes:** Katheryn Melissa Contento Maldonado; Juan Alberto
> Calopino Martinez; Wilson Patricio Palma Samaniego; Bryan Gustavo Troya Velez.
>
> **Asignatura:** Simulación — **Carrera:** Computación — **Docente:** Ing. José
> O. Guamán Q. — **Ciclo:** Quinto — **Fecha:** 15 y 16 de octubre de 2026.

---

## 1. Descripción del problema y propósito de la simulación

Los sistemas de líneas de espera (bancos, cajeros, ventanillas de atención,
servidores de red, etc.) reciben clientes de forma aleatoria y los atienden con
un tiempo de servicio también aleatorio. Cuando el ritmo de llegadas se acerca a
la capacidad de atención, la cola crece y los tiempos de espera aumentan de forma
acelerada.

El modelo **M/M/1** es el modelo más sencillo que representa esta situación:
llegadas de Poisson, tiempos de servicio exponenciales y un único servidor que
atiende por orden de llegada (FIFO). Su solución analítica es conocida, lo que lo
convierte en un excelente punto de partida para **comprobar** que una simulación
de eventos discretos reproduce el comportamiento descrito por la teoría.

El propósito de esta práctica es construir la simulación, medir experimentalmente
el desempeño del sistema y contrastar los resultados simulados con los valores
teóricos.

## 2. Objetivo general

Desarrollar una aplicación modular en Python que simule un sistema de líneas de
espera M/M/1 mediante SimPy, calcule sus métricas teóricas y simuladas, las
presente de forma comparativa y permita visualizar la evolución de la cola y la
distribución de los tiempos de espera a través de una interfaz web local.

## 3. Tecnologías utilizadas

| Tecnología | Uso dentro del proyecto |
|---|---|
| Python | Lenguaje de programación del proyecto |
| SimPy | Motor de simulación de eventos discretos (reloj, llegadas, recurso servidor) |
| NumPy | Generación de variables aleatorias exponenciales y cálculos estadísticos |
| Matplotlib | Construcción de las gráficas (evolución de la cola, histogramas, comparaciones) |
| Streamlit | Interfaz gráfica web local en español |
| unittest | Pruebas automatizadas (de la biblioteca estándar de Python) |

## 4. Descripción del modelo M/M/1

* **Primera M**: los tiempos entre llegadas siguen una distribución exponencial
  (equivalentes a un proceso de llegadas de Poisson).
* **Segunda M**: los tiempos de servicio siguen una distribución exponencial.
* **1**: existe un único servidor.
* **Disciplina FIFO**: primero en llegar, primero en ser atendido.
* Los tiempos entre llegadas y de servicio se expresan en la misma unidad de
  tiempo (por ejemplo, minutos).

Cada cliente se representa con: identificador, instante de llegada, inicio del
servicio, tiempo de espera, duración del servicio, instante de salida y tiempo
total en el sistema.

## 5. Parámetros y escenarios disponibles

| Parámetro | Significado |
|---|---|
| `lambda_rate` (λ) | Tasa media de llegada de clientes (clientes por unidad de tiempo) |
| `mu_rate` (μ) | Tasa media de servicio (clientes por unidad de tiempo) |
| `num_customers` | Cantidad de clientes generados en cada ejecución |
| `seed` | Semilla del generador aleatorio, para reproducir los resultados |

Escenarios obligatorios definidos en la guía de la práctica:

| Escenario | λ | μ | Característica | ρ = λ/μ |
|---|---:|---:|---|---:|
| 1 | 2.0 | 3.0 | Sistema estable | 0.667 |
| 2 | 2.5 | 3.0 | Mayor utilización | 0.833 |
| 3 | 2.9 | 3.0 | Cerca de la saturación | 0.967 |

La interfaz permite ejecutar **un escenario individual** o **los tres escenarios**
en una misma operación para compararlos. La cantidad de clientes y la semilla se
pueden modificar desde el panel de configuración sin alterar los valores de λ y μ
de los escenarios obligatorios.

## 6. Fórmulas de las métricas teóricas

Las métricas teóricas se calculan en `model/metrics.py`, en estado estacionario y
solo cuando el sistema es estable (λ < μ):

| Métrica | Fórmula |
|---|---|
| Utilización del servidor | `ρ = λ / μ` |
| Clientes promedio en el sistema | `L = λ / (μ − λ)` |
| Clientes promedio en la cola | `Lq = λ² / (μ · (μ − λ))` |
| Tiempo promedio en el sistema | `W = 1 / (μ − λ)` |
| Tiempo promedio en la cola | `Wq = λ / (μ · (μ − λ))` |
| Condición de estabilidad | `λ < μ` |

Si las tasas no son positivas o si λ ≥ μ, el programa **no** calcula las métricas
estacionarias y muestra un mensaje comprensible en español.

## 7. Arquitectura MVC y responsabilidades de los archivos

El proyecto aplica una arquitectura **MVC** sencilla, sin capas ni patrones
adicionales:

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Punto de entrada. Conecta la vista con el controlador; no contiene lógica del modelo |
| `model/queue_model.py` | Modelo de simulación: crea el entorno SimPy, el recurso de capacidad 1, genera clientes y registra sus tiempos |
| `model/metrics.py` | Métricas teóricas y validación de tasas (no depende de la interfaz) |
| `controller/simulation_controller.py` | Coordina: define los escenarios, valida parámetros, ejecuta el modelo y prepara la tabla comparativa |
| `view/dashboard.py` | Vista: encabezado, panel de configuración, tarjetas, tablas y gráficas con Streamlit y Matplotlib |
| `tests/test_metrics.py` | Pruebas de las métricas teóricas y de la validación de tasas |
| `tests/test_simulation.py` | Pruebas de la simulación, del controlador y de la separación MVC |

El **modelo** no importa Streamlit: puede ejecutarse sin interfaz gráfica. El
**controlador** no dibuja nada, solo coordina. La **vista** no simula, solo
presenta. Esta separación se comprueba en `tests/test_simulation.py`
(clase `TestArchitecture`).

### Decisiones de simulación documentadas

* **Cantidad fija de clientes**: cada ejecución genera exactamente
  `num_customers` clientes y la simulación avanza hasta que **todos** terminan su
  servicio. Por eso ninguna métrica excluye arbitrariamente a clientes que aún
  esperaban en la cola.
* **Intervalo de observación**: los promedios temporales se calculan en el
  intervalo `[0, T]`, donde `T` es el instante en que el último cliente termina su
  servicio.
* **Tamaño promedio de la cola (Lq)**: se integra el número de clientes esperando
  a lo largo del tiempo y se divide el área acumulada entre `T`. Se actualiza con
  eventos reales del modelo (cada vez que un cliente empieza a esperar o empieza a
  ser atendido), no con muestreos periódicos.
* **Utilización experimental**: se integra el tiempo en que el servidor estuvo
  ocupado y se divide entre `T`.
* **Aleatoriedad reproducible**: cada ejecución usa su propio generador
  `numpy.random.default_rng(seed)`. Al comparar los tres escenarios se utiliza la
  misma semilla y la misma cantidad de clientes para todos.
* **L y Lq no son lo mismo**: `L` incluye al cliente que está siendo atendido;
  `Lq` cuenta únicamente a quienes esperan en la cola.

## 8. Árbol real de carpetas

```
ape3-simulacion-mm1/            <- raíz del proyecto (el nombre local puede variar)
├── app.py                      <- punto de entrada de Streamlit
├── model/
│   ├── __init__.py
│   ├── queue_model.py          <- simulación de eventos discretos con SimPy
│   └── metrics.py              <- métricas teóricas y validación de tasas
├── controller/
│   ├── __init__.py
│   └── simulation_controller.py<- escenarios, validación y tabla comparativa
├── view/
│   ├── __init__.py
│   └── dashboard.py            <- encabezado, controles, tablas y gráficas
├── tests/
│   ├── __init__.py
│   ├── test_metrics.py         <- pruebas de las métricas teóricas
│   └── test_simulation.py      <- pruebas de la simulación y del controlador
├── requirements.txt            <- dependencias directas con versiones verificadas
├── .gitignore                  <- excluye entornos virtuales, cachés y temporales
├── README.md                   <- este documento
├── indicaciones/               <- material de trabajo (no se sube al repositorio)
│   ├── ape_guia simulacion semana 3-firmado-signed.pdf
│   └── indicaciones del docente.md
├── informe/                    <- informe de la práctica (no se sube al repositorio)
│   ├── doc.md                  <- fuente Markdown del informe
│   ├── documento final.docx    <- informe convertido con Pandoc
│   ├── img/                    <- gráficas generadas por la simulación
│   ├── plantuml-images/        <- diagramas PlantUML
│   ├── resultados.json         <- resultados crudos de la ejecución de referencia
│   ├── _generate_evidence.py   <- script que regenera tablas, gráficas y resultados
│   └── convert-to-docx.ps1     <- script de conversión a DOCX con Pandoc
└── recursos/                   <- material interno del equipo (no se sube al repositorio)
    ├── integrantes.md
    ├── reglas_internas_simulacion.md
    └── COMO-SUBIR-A-GITHUB.md
```

Las carpetas `indicaciones/`, `informe/` y `recursos/` son material de trabajo
del equipo: el repositorio de Git solo debe contener el código, las pruebas,
`requirements.txt`, `.gitignore` y `README.md`.

## 9. Requisitos previos

* Python **3.12 o superior** (el proyecto fue verificado con Python 3.12 y 3.14).
* `pip` actualizado.
* Conexión a internet **solo** para instalar las dependencias. Una vez instaladas,
  la aplicación funciona sin conexión.

Comprobar la versión instalada:

```bash
python --version
```

En Windows puede usarse el lanzador `py` (por ejemplo `py -3.12 -m venv .venv`).

## 10. Instalación paso a paso

1. Obtener el proyecto (cuando el grupo cree el repositorio, sería `git clone <url>`).
2. Entrar en la carpeta del proyecto:

```bash
cd simulacion_mm1
```

3. Crear el entorno virtual:

### Linux / macOS

```bash
python3 -m venv .venv
```

### Windows (PowerShell)

```powershell
python -m venv .venv
```

### Windows (símbolo del sistema / CMD)

```bat
python -m venv .venv
```

Si en el equipo hay varias versiones de Python instaladas, conviene elegir
explícitamente una que sea 3.12 o superior, por ejemplo
`py -3.12 -m venv .venv`.

> **Importante:** un entorno virtual no se puede “cambiar de versión de Python”
> en el mismo directorio. Si el `.venv` ya existía y se vuelve a ejecutar
> `venv` sobre él, el intérprete se reemplaza pero las dependencias antiguas
> permanecen y aparecen errores como
> `ModuleNotFoundError: No module named 'numpy._core._multiarray_umath'`.
> En ese caso hay que **eliminar la carpeta `.venv`** y crearla otra vez desde cero.

## 11. Activación del entorno virtual

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (símbolo del sistema / CMD)

```bat
.venv\Scripts\activate.bat
```

Cuando el entorno está activo, la terminal muestra `(.venv)` al comienzo de la
línea. Para salir del entorno se ejecuta `deactivate`.

## 12. Instalación de dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

La carpeta del entorno virtual (`.venv/`) **no** se sube al repositorio: ya está
excluida en `.gitignore`.

### Contenido de `requirements.txt`

```
simpy==4.1.2
numpy==2.5.4
matplotlib==3.11.2
streamlit==1.66.0
```

Son las cuatro dependencias directas del proyecto, con versiones que se
instalaron y probaron en un entorno virtual limpio (Python 3.12 y Python 3.14).

## 13. Ejecución de las pruebas

Las pruebas usan la biblioteca estándar `unittest`, por lo que no requieren
instalar nada adicional. Desde la **raíz del proyecto**, con el entorno virtual
activado:

```bash
python -m unittest -v
```

También se pueden ejecutar con descubrimiento explícito:

```bash
python -m unittest discover -s tests -t . -v
```

Resultado esperado: **20 pruebas ejecutadas, todas correctas (`OK`)**. Las pruebas
comprueban, entre otras cosas, que las métricas teóricas de λ = 2.0 y μ = 3.0 son
exactas, que la utilización se calcula como λ/μ, que se rechaza un sistema
inestable (λ ≥ μ), que se genera la cantidad de clientes solicitada, que todos son
atendidos, que los tiempos son coherentes, que el servidor no atiende a dos
clientes a la vez, que la misma semilla reproduce los resultados y que los tres
escenarios obligatorios se ejecutan correctamente.

## 14. Inicio de la aplicación

Con el entorno virtual activado y desde la raíz del proyecto:

```bash
streamlit run app.py
# python -m streamlit run app.py
```

Streamlit mostrará en la terminal una dirección local similar a:

```
Local URL: http://localhost:8501
```

Abrir esa dirección en el navegador. Para detener la aplicación, presionar
`Ctrl + C` en la terminal.

## 15. Uso básico de la interfaz

1. **Panel de configuración (barra lateral)**
   * *Escenario a ejecutar*: Escenario 1, Escenario 2, Escenario 3 o
     “Comparar los tres escenarios”.
   * *Cantidad de clientes*: por defecto 1000. Con más clientes los resultados
     suelen acercarse más a la teoría, pero la simulación tarda un poco más.
   * *Semilla aleatoria*: por defecto 42. Si se cambia, cambian los resultados;
     si se repite la misma semilla con la misma configuración, los resultados
     son idénticos.
   * *Iniciar simulación*: ejecuta el modelo.
2. **Resultados principales**: tarjetas con la utilización teórica, el tiempo
   promedio de espera simulado (Wq), el tamaño promedio de la cola simulado (Lq)
   y la cantidad de clientes atendidos.
3. **Tabla comparativa**: columnas teóricas y simuladas para cada escenario. Las
   columnas cuyo nombre termina en *teórica* provienen de las fórmulas; el resto
   proviene de la simulación.
4. **Visualización**: evolución del tamaño de la cola en el tiempo e histograma de
   los tiempos de espera. Al comparar los tres escenarios se añaden las gráficas
   comparativas de Wq y de Lq.
5. **Datos de clientes**: sección desplegable con la tabla individual (llegada,
   inicio de servicio, espera, servicio, salida y tiempo en el sistema). Se
   muestran como máximo los primeros 200 clientes para no saturar la interfaz.

## 16. Interpretación de resultados y gráficas

* **Evolución del tamaño de la cola**: muestra cuántos clientes esperan en cada
  instante. La línea discontinua es el valor teórico de `Lq`. Cuanto más cerca
  está λ de μ, más alta y más irregular es la serie.
* **Histograma de tiempos de espera**: distribución de las esperas individuales.
  La línea negra discontinua es `Wq` teórica y la línea roja la espera promedio
  simulada. En el escenario 1 muchas observaciones valen cero (el servidor suele
  estar libre); en el escenario 3 la distribución se desplaza hacia la derecha.
* **Gráficas comparativas**: barras grises para el valor teórico y azules para el
  simulado, en los tres escenarios. Permiten ver cómo crecen Wq y Lq al aumentar
  λ.
* **ρ (utilización)**: proporción del tiempo en que el servidor está ocupado. En
  el escenario 3, ρ ≈ 0.967, es decir, el servidor está ocupado casi todo el
  tiempo y por eso la cola es mucho mayor.

## 17. Limitaciones del modelo y diferencias entre teoría y simulación

* **Variabilidad aleatoria**: la simulación usa números aleatorios, por lo que
  cada ejecución produce valores distintos. Las diferencias disminuyen al aumentar
  la cantidad de clientes.
* **Tamaño de la muestra**: con pocos clientes (por ejemplo 100) las diferencias
  frente a la teoría pueden ser grandes; con 10 000 o más suelen ser pequeñas.
* **Periodo transitorio**: la teoría describe el estado estacionario, pero la
  simulación comienza con el servidor vacío. Ese arranque “a cola vacía” hace que
  los promedios simulados sean ligeramente menores que los teóricos.
* **Cerca de la saturación**: en el escenario 3 (ρ ≈ 0.967) la cola es muy
  sensible al azar y a la cantidad de clientes; se necesitan simulaciones largas
  para acercarse al valor teórico. Que el resultado simulado sea menor que el
  teórico en este escenario es esperable y no indica un error del modelo.
* **Delimitación de la simulación**: los promedios temporales se calculan en el
  intervalo `[0, T]`, con `T` = instante en que sale el último cliente. Otra
  delimitación razonable (por ejemplo, empezar a observar tras el primer cliente)
  daría valores ligeramente distintos.
* **Errores numéricos**: los tiempos se manejan en punto flotante; las
  comparaciones internas usan tolerancias muy pequeñas.
* **El modelo no incluye**: capacidad máxima de la cola, prioridades, varios
  servidores, clientes que se retiran sin ser atendidos ni tiempos de servicio
  no exponenciales.

En resumen: **no se exige que la simulación coincida exactamente con la teoría**.
Lo que se busca es que los valores simulados sean coherentes y se aproximen a los
teóricos cuando la simulación es suficientemente larga.

## 18. Uso de Git y recomendaciones para el trabajo colaborativo

El repositorio todavía no existe; cuando el grupo lo cree, estas son las
recomendaciones:

1. Inicializar el repositorio en la raíz del proyecto (`git init`) y hacer el
   primer commit con el código, las pruebas, `requirements.txt`, `.gitignore` y
   `README.md`.
2. **No** agregar `.venv/`, `venv/`, `__pycache__/` ni ninguna carpeta de
   dependencias: el archivo `.gitignore` ya las excluye.
3. Trabajar con una rama por integrante, por ejemplo:

```bash
git checkout -b feature/nombre_integrante
```

4. Integrar los cambios en `develop` y finalmente en `main`, según la estrategia
   que acuerde el grupo.
5. Antes de cada commit revisar `git status` y `git diff` para no subir archivos
   temporales ni datos personales.
6. Los commits deben realizarlos los integrantes del grupo; la asistencia de IA
   se documenta en el README, no como autor de los commits.

## 19. Declaración del uso de inteligencia artificial

Únicamente se utilizó [OpenCode](https://opencode.ai) para la redacción de este README, incluso para generar las tablas. Todo el desarrollo, análisis, cálculos, ejecución y validación fueron realizados por los integrantes del grupo.
