# Práctica 01: Construcción y Simulación Computacional de un Modelo Matemático Meteorológico

**Asignatura:** Simulación (Ciclo 5)  
**Carrera:** Computación - Universidad Nacional de Loja  
**Docente:** Ing. José O. Guamán Q.  
**Estudiante:** Katheryn M. Contento M. 

---

## 1. Descripción del Proyecto

Este proyecto implementa y simula un modelo matemático meteorológico para predecir la probabilidad de lluvia durante un periodo de 24 horas. El sistema está desarrollado en **Python 3** bajo principios de **Clean Architecture** y el patrón de diseño **Strategy**, separando desacopladamente las reglas de negocio, los algoritmos de simulación y la representación gráfica.

---

## 2. Arquitectura de Software y Patrones de Diseño

El proyecto no utiliza un script monolítico en un solo archivo, sino una estructura modular que cumple con los principios SOLID:

- **Strategy Pattern (Patrón Estrategia):**
  - `ITemperatureStrategy`: Define la forma de calcular el factor de temperatura $T_f$.
  - `IRainModelStrategy`: Permite alternar dinámicamente entre el **Modelo Base** lineal y el **Modelo Ajustado** sinérgico sin alterar el motor de simulación.
- **Single Responsibility Principle (SRP):** Cada módulo posee una única responsabilidad (`plotter` solo grafica, `console_view` solo presenta datos, `simulator` solo calcula).

---

## 3. Justificación del Cálculo de $T_f$ y Modelo Ajustado

### A. Cálculo de $T_f$ para Temperaturas No Tabuladas ($15^\circ\text{C}$ y $17^\circ\text{C}$)
Se aplicó **Interpolación Lineal Continua** debido a que la tabla de parámetros presenta una variación constante de $-0.05$ en $T_f$ por cada $1^\circ\text{C}$ de incremento en la temperatura. La función continua derivada es:
$$T_f(T) = 1.50 - 0.05 \cdot T$$

- Para **$15^\circ\text{C}$**: $T_f = 1.50 - 0.05(15) = 0.75$
- Para **$17^\circ\text{C}$**: $T_f = 1.50 - 0.05(17) = 0.65$

### B. Justificación Académica del Modelo Ajustado
El modelo base propone la fórmula lineal $I = 0.5H + 0.3N + 0.2T_f$. Se propone el modelo ajustado sinérgico:
$$I_{\text{ajustado}} = 0.40H + 0.40N + 0.20T_f + 0.10(H \cdot N)$$

#### Referencias Científicas:
1. **Muller et al. (2009) - *Geophysical Research Letters*:** Demuestra que la relación entre la humedad atmosférica y la precipitación no es lineal, presentando una aceleración (*pickup*) cuando la humedad relativa y la nubosidad se aproximan a la saturación simultáneamente.
2. **Sundqvist (1989) - *Atmospheric Research*:** En los modelos numéricos de predicción del tiempo (NWP), la formación de precipitación depende del producto interactivo entre la humedad relativa ($H$) y la fracción de nubes ($N$).
3. **Ameen et al. (2023) - *Fuzzy Logic Rainfall Models*:** Los modelos de inferencia difusa demuestran que las reglas cruzadas (`AND`) reducen los errores de predicción durante eventos severos.

---

## 4. Resultados de la Simulación

### Tabla 1: Modelo Base (Lineal)
| Hora | Hum(%) | Nub(%) | Temp(°C) | H | N | $T_f$ | Índice ($I$) | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 06:00 | 65 | 40 | 14 | 0.65 | 0.40 | 0.80 | 0.6050 | Lluvia probable |
| 08:00 | 70 | 50 | 16 | 0.70 | 0.50 | 0.70 | 0.6400 | Lluvia probable |
| 10:00 | 68 | 45 | 18 | 0.68 | 0.45 | 0.60 | 0.5950 | Baja posibilidad |
| 12:00 | 60 | 30 | 22 | 0.60 | 0.30 | 0.40 | 0.4700 | Baja posibilidad |
| 14:00 | 75 | 70 | 20 | 0.75 | 0.70 | 0.50 | 0.6850 | Lluvia probable |
| 16:00 | 85 | 85 | 18 | 0.85 | 0.85 | 0.60 | 0.8000 | Lluvia |
| 18:00 | 92 | 95 | 16 | 0.92 | 0.95 | 0.70 | 0.8850 | Lluvia |
| 20:00 | 88 | 90 | 17 | 0.88 | 0.90 | 0.65 | 0.8400 | Lluvia |
| 22:00 | 80 | 75 | 15 | 0.80 | 0.75 | 0.75 | 0.7750 | Lluvia |

### Tabla 2: Modelo Ajustado (Sinérgico)
| Hora | Hum(%) | Nub(%) | Temp(°C) | H | N | $T_f$ | Índice ($I$) | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 06:00 | 65 | 40 | 14 | 0.65 | 0.40 | 0.80 | 0.6060 | Lluvia probable |
| 08:00 | 70 | 50 | 16 | 0.70 | 0.50 | 0.70 | 0.6550 | Lluvia probable |
| 10:00 | 68 | 45 | 18 | 0.68 | 0.45 | 0.60 | 0.6026 | Lluvia probable |
| 12:00 | 60 | 30 | 22 | 0.60 | 0.30 | 0.40 | 0.4580 | Baja posibilidad |
| 14:00 | 75 | 70 | 20 | 0.75 | 0.70 | 0.50 | 0.7325 | Lluvia probable |
| 16:00 | 85 | 85 | 18 | 0.85 | 0.85 | 0.60 | 0.8723 | Lluvia |
| 18:00 | 92 | 95 | 16 | 0.92 | 0.95 | 0.70 | 0.9754 | Lluvia |
| 20:00 | 88 | 90 | 17 | 0.88 | 0.90 | 0.65 | 0.9212 | Lluvia |
| 22:00 | 80 | 75 | 15 | 0.80 | 0.75 | 0.75 | 0.8300 | Lluvia |

---

## 5. Respuestas a las Preguntas de Control

1. **¿Qué es un modelo matemático?**  
   Es una representación abstracta y simplificada de un sistema o fenómeno del mundo real mediante expresiones, variables y relaciones matemáticas, orientada a analizar, comprender o predecir su comportamiento.
2. **¿Cuál es la diferencia entre variable y parámetro?**  
   - **Variable:** Mapea cantidades que cambian dinámicamente durante la simulación (ej. Humedad $H$, Nubosidad $N$, Índice $I$).
   - **Parámetro:** Constante o coeficiente fijo que define las características estructurales del modelo (ej. los pesos $0.5, 0.3, 0.2$).
3. **¿Qué representa $P_0$?**  
   Representa la condición o población inicial del sistema en el instante de tiempo de inicio $t = 0$ dentro de modelos de crecimiento dinámico/exponencial.
4. **¿Qué ocurre cuando $r < 0$?**  
   Representa una tasa de crecimiento negativa, lo que provoca un decrecimiento o decaimiento exponencial en el sistema a lo largo del tiempo.
5. **¿Qué limitaciones tiene el modelo exponencial?**  
   Asume que el crecimiento puede continuar de forma indefinida sin restricciones, ignorando la capacidad de carga del entorno ($K$), la limitación de recursos y los factores de saturación ambiental.

---

## 6. Instrucciones de Ejecución

```bash
# 1. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la simulación
python3 main.py
```
## 7. Declaración de Integridad Académica y Uso de Inteligencia Artificial

En cumplimiento con las políticas de honestidad académica de la institución y el límite permitido (máximo **20% de asistencia de IA**), se declara de manera explícita la distribución del trabajo desarrollado en esta práctica:

### Proporción de Trabajo:
- **Trabajo Autónomo del Estudiante:** 85%
- **Asistencia Puntual con IA:** 15% (Dentro del margen normativo)

### Aporte y Desarrollo del Estudiante (85%):
1. **Análisis y Planteamiento:** Interpretación de los requerimientos de la guía de práctica, definición de variables, normalización de datos ($H, N$) y resolución analítica de casos de borde.
2. **Modelado Matemático e Interpolación:** Deducción analítica de la ecuación de interpolación lineal continua para el factor de temperatura $T_f(T) = 1.50 - 0.05 \cdot T$ correspondiente a $15^\circ\text{C}$ y $17^\circ\text{C}$.
3. **Arquitectura de Software y Patrones:** Selección de la estructura desacoplada (*Clean Architecture*) y aplicación del patrón de diseño **Strategy** para alternar entre los algoritmos de simulación.
4. **Construcción e Implementación:** Desarrollo e implementación manual de clases, interfaces abstractas, clases de datos (`@dataclass`) y el orquestador principal (`simulator.py`).
5. **Ajuste del Modelo y Preguntas:** Propuesta del factor de interacción sinérgica ($0.10 \cdot H \cdot N$) para el modelo ajustado y resolución de las preguntas de control.
6. **Configuración del Entorno y Git:** Configuración del entorno virtual en Linux, gestión de dependencias y control de versiones con Git y GitHub.

### Asistencia Puntual de Inteligencia Artificial (15%):
- **Consultas de Sintaxis:** Asistencia puntual en la sintaxis de tipos en Python (`typing.List`) y uso de clases base abstractas (`abc.ABC`).
- **Formateo de Tablas:** Apoyo en la maquetación en sintaxis Markdown para la presentación ordenada de tablas de resultados en la documentación.
- **Búsqueda de Literatura:** Sugerencia de artículos académicos (Muller et al., Sundqvist) para respaldar la fundamentación física del modelo ajustado.