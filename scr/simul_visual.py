# python -m scr.simul_visual

import sys
import random
import pygame
from time import sleep

# Seleccionar mapa visual: small o big
from scr.config_small import conexiones, nodos, aristas, VENTANA, RELOJ, FPS, \
    dibujar_tablero, dibujar_piezas, cartel, mostrar_texto

# Algoritmos
from scr.alg_astar import gato_move_astar, raton_move_astar
from scr.alg_minimax import gato_move_minimax, raton_move_minimax
from scr.alg_random import gato_move_random, raton_move_random


# ==================== CONFIGURAR ALGORITMOS ====================
MODO_GATO = "minimax"   # opciones: astar / minimax / random
MODO_RATON = "astar"    # opciones: astar / minimax / random
# ===============================================================


def mover_raton_auto(pos_gato, pos_raton, queso, final, tiene_queso):
    if MODO_RATON == "astar":
        return raton_move_astar(conexiones, nodos, pos_gato, pos_raton, queso, final, tiene_queso)
    elif MODO_RATON == "minimax":
        return raton_move_minimax(conexiones, nodos, pos_gato, pos_raton)
    else:
        return raton_move_random(conexiones, pos_gato, pos_raton)


def mover_gato_auto(pos_gato, pos_raton):
    if MODO_GATO == "astar":
        return gato_move_astar(conexiones, nodos, pos_gato, pos_raton)
    elif MODO_GATO == "minimax":
        return gato_move_minimax(conexiones, nodos, pos_gato, pos_raton)
    else:
        return gato_move_random(conexiones, pos_gato, pos_raton)


def iniciar_simulacion():
    nodos_ids = list(nodos.keys())

    pos_raton = random.choice(nodos_ids)
    pos_gato = random.choice([n for n in nodos_ids if n != pos_raton])
    queso = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato)])
    final = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato, queso)])

    tiene_queso = False
    turno = "raton"
    terminado = False

    pasos = 0
    MAX_PASOS = 200

    while not terminado:
        RELOJ.tick(FPS)

        # Eventos para poder salir
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Movimiento automático
        if turno == "raton":
            pos_raton = mover_raton_auto(pos_gato, pos_raton, queso, final, tiene_queso)
            turno = "gato"
        else:
            pos_gato = mover_gato_auto(pos_gato, pos_raton)
            turno = "raton"

        pasos += 1
        sleep(0.4)  # para que se vea la animación

        # Lógica del juego
        if pos_gato == pos_raton:
            cartel("¡GAME OVER! El gato atrapó al ratón.")
            terminado = True

        if pos_raton == queso and not tiene_queso:
            tiene_queso = True

        if pos_raton == final and tiene_queso:
            cartel("¡El ratón ganó!", (200, 255, 200))
            terminado = True

        if pasos >= MAX_PASOS:
            cartel("Empate por tiempo")
            terminado = True

        # Dibujo en pantalla
        dibujar_tablero(VENTANA, nodos, aristas, pos_raton, final, tiene_queso, queso)
        dibujar_piezas(VENTANA, nodos, pos_gato, pos_raton)
        mostrar_texto(f"Gato: {MODO_GATO} | Ratón: {MODO_RATON}", 10)
        pygame.display.flip()


if __name__ == "__main__":
    iniciar_simulacion()
