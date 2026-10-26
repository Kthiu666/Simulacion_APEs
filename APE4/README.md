# APE 4 Modelo SIR con escenarios

Python con SimPy y un modelo nativo NetLogo 7.0.4, conectados mediante CSV.
No se implementa Java por el alcance acordado.

## Probar los tres casos en NetLogo

Abre `netlogo/modelo_sir_netlogo.nlogox`. Si tenías una versión abierta, ciérrala y
vuelve a abrir el archivo actualizado; no guardes encima una copia antigua.

1. Pulsa **MALO**, **NORMAL APE** o **FAVORABLE**. Se aplican los parámetros y se
   reinicia la población. Cada botón restaura la semilla 42.
2. Usa **EJECUTAR / PAUSAR** o **UN PASO** para observar la evolución nativa.
3. Pulsa **CARGAR PYTHON** para importar el CSV ya incluido del caso seleccionado.
4. Pulsa **COMPARAR** para completar NetLogo y mostrar ambas herramientas.
5. **EXPORTAR NETLOGO** guarda su corrida y sus parámetros en la carpeta del caso.

| Caso | Contagio β | Recuperación γ | Interpretación del experimento |
|---|---:|---:|---|
| Malo | 0.60 | 0.05 | Mayor transmisión y recuperación lenta |
| Normal APE | 0.30 | 0.10 | Parámetros originales de la guía |
| Favorable | 0.10 | 0.30 | Menor transmisión y recuperación rápida |

Los tres usan N=100, I(0)=5, R(0)=0, 100 pasos, un contacto por infectado y semilla 42.
Son escenarios ilustrativos. Favorable es el mejor de los tres casos propuestos,
no una optimización matemática ni una garantía para toda realización aleatoria.

Los datos incluidos están listos para usarse. Para regenerar los tres casos
Python y una gráfica que los compara, desde `ape4_sir` ejecuta:

```bash
.venv/bin/python escenarios.py
```

Consulta `graficas/escenarios/comparacion_escenarios.png` y
`graficas/escenarios/resumen_escenarios.csv`.

## Cambiar valores libremente en NetLogo

1. Pausa el botón **EJECUTAR / PAUSAR** si sigue activo.
2. Edita los campos de la parte superior:

| Campo | Significado | Valores permitidos |
|---|---|---|
| n-personas | Población total N | Entero, al menos 2 |
| infectados-iniciales | I(0) | Entero entre 0 y N |
| prob-contagio | β por contacto susceptible | Entre 0 y 1 |
| prob-recuperacion | γ por infectado y paso | Entre 0 y 1 |
| duracion | Cantidad de pasos | Entero, 0 o mayor |
| contactos | Contactos distintos por infectado y paso | Entero de 1 a N−1 |
| semilla | Repetibilidad de la corrida | Entero de −2147483648 a 2147483647 |

3. Pulsa **REINICIAR / APLICAR**. Los cambios se aplican juntos desde t=0.
4. Ejecuta la simulación. La población, las curvas y sus ejes se adaptan a N y T.

Modificar controles durante una corrida exige reiniciar: no se mezclan reglas
viejas y nuevas. Los botones de escenario también reinician; pausa antes de
usarlos. Reiniciar limpia las series de la sesión, pero no borra archivos.

### Comparar un caso personalizado con Python

Puedes experimentar en NetLogo sin ejecutar Python. Para comparar las dos
herramientas, genera Python con **los mismos siete valores**. Por ejemplo:

```bash
.venv/bin/python main.py --poblacion 200 --infectados 10 --beta 0.2 --gamma 0.15 --pasos 150 --contactos 2 --semilla 7
```

Configura esos valores en NetLogo, pulsa REINICIAR / APLICAR y luego **CSV ACTUAL**.
Este botón carga `netlogo/resultados_python.csv`. Después pulsa COMPARAR y EXPORTAR
NETLOGO. Para generar la figura externa:

```bash
.venv/bin/python comparar.py
```

El campo `archivo-python` admite otra carpeta terminada en `resultados_python.csv`;
el archivo de parámetros debe encontrarse junto a él. Si los valores no coinciden,
se rechaza la carga para no presentar una comparación equivocada.

## Ejecutar un perfil desde Python

```bash
.venv/bin/python main.py --escenario malo
.venv/bin/python main.py --escenario normal
.venv/bin/python main.py --escenario favorable
```

Un perfil exacto se guarda en `netlogo/escenarios/<caso>/` y sus gráficas en
`graficas/escenarios/<caso>/`. Si añades valores que modifican el perfil, se trata
como una corrida personalizada y se guarda en la carpeta `netlogo/` por defecto.
`--salida` y `--graficas` permiten elegir explícitamente otras ubicaciones.

Tras exportar el mismo caso desde NetLogo, compáralo por ejemplo con:

```bash
.venv/bin/python comparar.py --carpeta netlogo/escenarios/malo
```

Sin argumentos, `main.py` conserva los parámetros de la guía y genera la corrida
normal en `netlogo/`. Así se reproduce el caso base del informe.

## Archivos y sobrescritura

Cada carpeta de corrida contiene:

- `resultados_python.csv` y `resultados_netlogo.csv`: las cuatro columnas de la guía
  `tiempo,susceptibles,infectados,recuperados`; T+1 filas, incluido el estado inicial.
- `parametros_python.csv` y `parametros_netlogo.csv`: una fila con los siete valores
  de configuración. Se usan para comprobar que las curvas corresponden al mismo
  experimento, sin modificar el formato de los datos SIR.

Malo, normal y favorable están separados. Repetir una exportación sobrescribe los
archivos de esa carpeta. Copia una corrida antes si quieres conservarla con otra
semilla. No copies un CSV SIR sin su archivo de parámetros acompañante.

## Modelo común

Cada infectado original selecciona k personas diferentes, de forma uniforme entre
los otros N−1 individuos. Cada contacto susceptible tiene probabilidad β de
contagio. Cada infectado original tiene probabilidad γ de recuperarse por paso.
Se consulta el estado anterior y se escribe en una copia: los nuevos infectados
no contagian ni se recuperan ese mismo paso. Los contagios repetidos no duplican
personas. No hay nacimientos, muertes ni reinfección; siempre S+I+R=N.

Se registran todos los pasos, incluso tras la extinción. Las posiciones en NetLogo
son decorativas y el movimiento no altera el generador epidemiológico.
Usar la misma semilla reproduce el resultado dentro de cada herramienta, pero no
hace idénticas las secuencias entre Python y NetLogo.

## Instalación y comprobación

Requiere Python 3.10 o posterior y NetLogo 7.0.4 o compatible. Desde esta carpeta:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s pruebas -v
```

En Windows usa `.venv\Scripts\activate` y `python` en lugar de `.venv/bin/python`.

El modelo incluye experimentos BehaviorSpace `validacion`, `escenario-malo`,
`escenario-normal` y `escenario-favorable`. Ejemplo Linux desde `ape4_sir`:

```bash
/opt/netlogo/netlogo-headless.sh --model "$PWD/netlogo/modelo_sir_netlogo.nlogox" --experiment escenario-malo --table /tmp/malo.csv --threads 1
```

El informe existente corresponde al caso normal de la guía. Los casos adicionales
son una extensión experimental; no sustituyen esa configuración en la evaluación.
