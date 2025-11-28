import sys
import random
import pygame

# Configuración del tablero (small o big)
from scr.config_small import *

# Algoritmos
from scr.alg.alg_astar import gato_move_astar, raton_move_astar
from scr.alg.alg_minimax import gato_move_minimax, raton_move_minimax
from scr.alg.alg_random import gato_move_random, raton_move_random


# MODO DE DECISIÓN DE LOS AGENTES

# Opciones: "astar", "minimax", "random"
MODO_GATO  = "minimax"
MODO_RATON = "astar"


# Estado Inicial del Juego

nodos_ids = list(nodos.keys())

pos_raton = random.choice(nodos_ids)
pos_gato  = random.choice([n for n in nodos_ids if n != pos_raton])

queso = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato)])
final = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato, queso)])

tiene_queso = False
turno = "raton"
game_over = False
victoria = False
inicio = pos_raton


# Funciones Auxiliares

def mover_raton_automatico():
    global pos_raton, tiene_queso

    if MODO_RATON == "astar":
        pos_raton_nuevo = raton_move_astar(conexiones, nodos, pos_gato, pos_raton, queso, final, tiene_queso)
    elif MODO_RATON == "minimax":
        pos_raton_nuevo = raton_move_minimax(conexiones, nodos, pos_gato, pos_raton)
    else:  # random
        pos_raton_nuevo = raton_move_random(conexiones, pos_gato, pos_raton)

    pos_raton = pos_raton_nuevo


def mover_gato_automatico():
    global pos_gato

    if MODO_GATO == "astar":
        pos_gato_nuevo = gato_move_astar(conexiones, nodos, pos_gato, pos_raton)
    elif MODO_GATO == "minimax":
        pos_gato_nuevo = gato_move_minimax(conexiones, nodos, pos_gato, pos_raton)
    else:  # random
        pos_gato_nuevo = gato_move_random(conexiones, pos_gato, pos_raton)

    pos_gato = pos_gato_nuevo


# Bucle Principal

while True:
    RELOJ.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

    # Movimiento automático
    if not (game_over or victoria):
        if turno == "raton":
            mover_raton_automatico()
            pygame.time.delay(600)  # <-- freno real
            turno = "gato"
        else:
            mover_gato_automatico()
            pygame.time.delay(600)  # <-- freno real
            turno = "raton"

    # Lógica del juego
    if not game_over and not victoria:

        # Captura
        if pos_gato == pos_raton:
            cartel("¡GAME OVER! El gato atrapó al ratón.")
            game_over = True

        # Ratón agarra queso
        if pos_raton == queso and not tiene_queso:
            tiene_queso = True

        # Ratón gana
        if pos_raton == final and tiene_queso:
            cartel("¡Ganaste! El ratón llegó con el queso", (200, 255, 200))
            victoria = True

    # Dibujo
    dibujar_tablero(VENTANA, nodos, aristas, inicio, final, tiene_queso, queso)
    dibujar_piezas(VENTANA, nodos, pos_gato, pos_raton)

    if game_over:
        mostrar_texto("Presiona cualquier tecla para reiniciar...", 50)
    elif victoria:
        mostrar_texto("Presiona cualquier tecla para volver a jugar...", 50)
    else:
        mostrar_texto(f"Turno: {turno.upper()} | Gato={MODO_GATO} | Ratón={MODO_RATON}", 40)
        if not tiene_queso:
            mostrar_texto("Busca el queso para revelar la meta", 75)
        else:
            mostrar_texto("La meta se ha revelado, ¡corre!", 75)

    pygame.display.flip()

    # Reinicio tras game over / victoria
    keys = pygame.key.get_pressed()
    if (game_over or victoria) and any(keys):
        pos_raton = random.choice(nodos_ids)
        pos_gato  = random.choice([n for n in nodos_ids if n != pos_raton])
        queso = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato)])
        final = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato, queso)])

        tiene_queso = False
        game_over = False
        victoria = False
        turno = "raton"
        inicio = pos_raton