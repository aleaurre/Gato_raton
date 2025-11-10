# 🐭 Gato y Ratón – Simulación Interactiva

Este proyecto implementa un **juego y simulación entre un gato y un ratón** sobre un tablero de nodos, con elementos como **queso, meta final y condiciones de colisión**.  
El objetivo es modelar comportamientos de agentes (ratón y gato) en distintos escenarios y posteriormente **automatizar las decisiones mediante algoritmos de búsqueda o aprendizaje**.
Justificación Teórica en: https://docs.google.com/document/d/1ps7sCIekX5k8wyKlOz_qVr1m89aT8EcIQt9Zv6oxTkM/edit?usp=sharing

---

## 📁 Estructura del proyecto

GATO_RATÓN/
├── assets/                # Imágenes utilizadas en el juego
│   ├── gato.png
│   ├── ratón.png
│   └── queso.png
│
├── docs/                  # Documentos teóricos y definiciones
│   ├── Def_Entrenamiento.pdf
│   └── Def_Problema.pdf
│
├── scr/                   # Scripts principales del modelo y experimentos
│   ├── alg_entrenamiento.py   # Algoritmos de simulación
│   ├── alg_estudio.py         # Análisis y pruebas
│   ├── config_big.py          # Configuración de tableros grandes
│   ├── config_small.py        # Configuración de tableros pequeños
│   └── modelado_juego.py      # Lógica del entorno y entidades
│
├── main.py                # Punto de entrada del juego/simulación
├── requirements.txt       # Dependencias necesarias
└── readme.md              # Descripción general del proyecto

---

## 🚀 Ejecución

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
    ````

2. Ejecutar el juego principal:
   ```bash
   python main.py
   ```

---

## 🧠 Créditos

Estudiantes universitarios de la carrera de grado de Ing. en Inteligencia Artificial y Ciencia de Datos.
Alexia Aurrecochea, Mercedes Barrutia, Sofía Craigdallie y Paula Blasco.
En el marco del curso de Algoritmos Avanzados de Búsqueda y Optimización.
Dictado por los docentes: Ing.Michel Pedrera e Ing.Pío Dos Santos