# Simulación — Prácticas APE 

Repositorio de las prácticas de la asignatura **Simulación** de la Carrera de
**Computación** — Universidad Nacional de Loja.

Cada práctica (APE) se organiza en una carpeta independiente con su código,
pruebas, dependencias y documentación propia.

## Prácticas incluidas

| APE | Tema | Tecnologías | Estado |
|---|---|---|---|
| [APE 1](APE1/) | Modelo matemático meteorológico: simulación del índice de lluvia | Python, NumPy, Matplotlib | ✅ Completada |
| [APE 2](APE2/) | Comparación de modelos determinísticos, estocásticos, discretos y continuos (crecimiento poblacional) | Python, NumPy, pandas, SciPy, Matplotlib | ✅ Completada |
| [APE 3](APE3/) | Sistema de líneas de espera M/M/1 | Python, SimPy, NumPy, Matplotlib, Streamlit | ✅ Completada |

## Estructura del repositorio

```
Simulacion_APEs/
├── README.md          <- este documento
├── .gitignore         <- exclusiones globales del repositorio
├── APE1/              <- práctica 1: modelo meteorológico (índice de lluvia)
│   ├── main.py        <- punto de entrada
│   ├── config/        <- parámetros y umbrales
│   ├── src/           <- dominio, estrategias, servicios y vistas
│   ├── tests/         <- pruebas del simulador
│   ├── requirements.txt
│   └── README.md      <- documentación completa de la práctica
├── APE2/              <- práctica 2: modelos de crecimiento poblacional
│   ├── modelos.py     <- los 4 modelos + estimación de r
│   ├── comparacion.py <- gráfica comparativa y CSV
│   ├── experimentos.py<- sensibilidad de r, sigma y dt
│   ├── resultados/    <- PNG y CSV de las ejecuciones
│   ├── requirements.txt
│   └── README.md      <- documentación completa de la práctica
└── APE3/              <- práctica 3: cola M/M/1
│   ├── app.py         <- punto de entrada
│   ├── model/         <- simulación y métricas teóricas
│   ├── controller/    <- escenarios y coordinación
│   ├── view/          <- dashboard Streamlit
│   ├── tests/         <- pruebas unittest
│   ├── informe/       <- informe PDF, gráficas y resultados
│   ├── requirements.txt
│   └── README.md      <- documentación completa de la práctica
```

## Requisitos generales

* Python **3.12 o superior**
* `pip` actualizado

Cada APE tiene su propio `requirements.txt`; las dependencias **no** se
comparten entre prácticas.

## Cómo ejecutar una práctica

Cada APE se ejecuta desde su propia carpeta. Ejemplo con la APE 3:

```bash
cd APE3
python -m venv .venv

# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
streamlit run app.py
```

Consulta el `README.md` de cada carpeta para instrucciones detalladas,
parámetros y resultados esperados.

## Convenciones para nuevas prácticas

Al agregar una nueva APE:

1. Crear la carpeta `APEn/` en la raíz del repositorio.
2. Incluir al menos: código fuente, `requirements.txt`, `.gitignore` propio y
   `README.md` con descripción, objetivos, instalación y uso.
3. Mantener la arquitectura **MVC** (`model/`, `controller/`, `view/`) cuando
   la práctica tenga interfaz.
4. Incluir las pruebas en `tests/` ejecutables con `python -m unittest`.
5. Agregar una fila en la tabla de prácticas de este archivo.
6. Usar mensajes de commit con el prefijo del APE, por ejemplo
   `feat(ape4): ...`, `docs(ape3): ...`.

## Asignatura

- **Asignatura:** Simulación
- **Carrera:** Computación
- **Ciclo:** Quinto
- **Docente:** Ing. José O. Guamán Q.

## Declaración del uso de inteligencia artificial

La asistencia de IA (OpenCode) se utilizó para la redacción de documentación y
el apoyo al desarrollo. Todo el análisis, los cálculos, las ejecuciones y la
validación de resultados fueron realizados por los integrantes del grupo.
