# 🐭🐱 Gato y Ratón — Búsqueda y Optimización en Grafos

Proyecto desarrollado para experimentar y comparar algoritmos de búsqueda y optimización en un entorno adversarial.
El juego simula la interacción entre un **ratón** que busca llegar con el queso a la meta, mientras un **gato** intenta atraparlo.

Los resultados del proyecto pueden visualizarse en el documento resultados.ipynb.

---

## 🎯 Objetivos

* Modelar el mapa como un grafo
* Implementar agentes autónomos con distintos algoritmos:
  * **Búsqueda A*** (heurística Manhattan)
  * **Minimax con poda Alfa-Beta**
  * **Estrategias estocásticas Random**
* Analizar el desempeño de cada estrategia.
* Visualizar la simulación en una interfaz gráfica interactiva.

---

## 🧩 Estructura del proyecto

GATO_RATÓN/
│
├── assets/              # Imágenes de las piezas
│   ├── gato.png
│   ├── queso.png
│   └── ratón.png
│
├── docs/                # Documentación del problema
│
├── scr/                 # Código fuente del proyecto
│   ├── alg/             # Algoritmos de movimiento
│   │   ├── alg_astar.py
│   │   ├── alg_minimax.py
│   │   ├── alg_random.py
│   │   ├── alg_estudio.py
│   │   └── alg_entrenamiento.py
│   │
│   ├── config_small.py  # Mapa pequeño (11 nodos)
│   ├── config_big.py    # Mapa grande (25 nodos)
│   ├── modelado_juego.py # Motor gráfico base
│   ├── simul_visual.py  # Simulación automática con visualización (Pygame)
│   ├── experimentos.py  # Simulación sin interfaz para análisis estadístico
│   └── test_astar.py    # Prueba básica del algoritmo A*
│
├── main.py              # Script para ejecutar una partida visual (puede ser manual/automática)
├── requirements.txt     # Dependencias del proyecto
├── resultados.ipynb     # Registro de resultados finales del Proyecto
└── README.md            # Este archivo

---

## 🚀 Instalación

1️⃣ Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv .venv
```

2️⃣ Activar entorno

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / MacOS
source .venv/bin/activate
```

3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶ Ejecución de la simulación

### Visual + automática (recomendado)

```bash
python -m scr.simul_visual
```

💡 Podés cambiar los algoritmos dentro del archivo:

```python
MODO_GATO = "minimax"   # opciones: astar | minimax | random
MODO_RATON = "astar"    # opciones: astar | minimax | random
```

También es posible usar:

```python
from scr.config_big import ...
```

para el tablero grande 🗺️

---

### Modo estadístico (sin visual)

```bash
python -m scr.experimentos
```

Este modo imprime en consola el desempeño de los algoritmos.

---

### Prueba mínima del A*

```bash
python -m scr.test_astar
```

---

## 🧠 Algoritmos implementados

| Algoritmo                | Agente       | Descripción                                             |
| ------------------------ | ------------ | ------------------------------------------------------- |
| A*                       | Gato / Ratón | Persigue objetivos en el grafo minimizando distancia    |
| Minimax + Alfa-Beta      | Gato / Ratón | Estrategia adversarial basada en juegos con dos agentes |
| Movimiento Random        | Gato / Ratón | Exploración estocástica para evitar ciclos o atascos    |
| Entrenamiento heurístico | Ratón        | Ajuste por grid-search de pesos de heurística           |
| BFS auxiliar             | Ambos        | Para calcular distancias reales en análisis             |

---

## 👩‍🔬 Créditos

**Alexia Aurrecochea, Mercedes Barrutia, Sofía Craigdallie y Paula Blasco.**
Estudiantes de Ingeniería en Inteligencia Artificial y Ciencia de Datos
Universidad Católica del Uruguay
En el marco del curso de Algoritmos Avanzados de Búsqueda y Optimización.
Supervisión: [📝 Ing.Michel Pedrera e Ing.Pío Dos Santos]
