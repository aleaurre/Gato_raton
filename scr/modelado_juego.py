import sys
import random
import pygame
from scr.config_small import *  # Modificar para cambiar de tablero
from scr.alg_astar import gato_move_astar
from scr.alg_minimax import gato_move_minimax

MODO_GATO = "astar"   # opciones: "astar" o "minimax"

TECLAS_VALIDAS = {
    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_q, pygame.K_e, pygame.K_z, pygame.K_c
}

# Estado Inicial del Juego
nodos_ids = list(nodos.keys())
pos_raton = random.choice(nodos_ids)
pos_gato = random.choice([n for n in nodos_ids if n != pos_raton])
queso = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato)])
final = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato, queso)])

inicio = pos_raton
tiene_queso = False
turno = "raton"
game_over = False
victoria = False


# Bucle Principal
while True:
    RELOJ.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            if not (game_over or victoria):
                if turno == "raton":
                    if event.key in TECLAS_VALIDAS:
                        pos_raton = mover_pieza(pos_raton, event.key, nodos, conexiones)
                        turno = "gato"


    # Movimiento automático del gato (A* o Minimax según modo)
    if not game_over and not victoria and turno == "gato":
        if MODO_GATO == "astar":
            pos_gato = gato_move_astar(conexiones, nodos, pos_gato, pos_raton)
        else:
            pos_gato = gato_move_minimax(conexiones, nodos, pos_gato, pos_raton)
        turno = "raton"


    # Lógica del Juego
    if not game_over and not victoria:
        if pos_gato == pos_raton:
            cartel("¡GAME OVER! El gato atrapó al ratón.")
            game_over = True

        if pos_raton == queso and not tiene_queso:
            tiene_queso = True

        if pos_raton == final and tiene_queso:
            cartel("¡Ganaste! El ratón llegó con el queso ", (200, 255, 200))
            victoria = True

  
    # Dibujo del Juego
    dibujar_tablero(VENTANA, nodos, aristas, inicio, final, tiene_queso, queso)
    dibujar_piezas(VENTANA, nodos, pos_gato, pos_raton)

    if game_over:
        mostrar_texto("Presiona cualquier tecla para reiniciar...", 50)
    elif victoria:
        mostrar_texto("Presiona cualquier tecla para volver a jugar...", 50)
    else:
        mostrar_texto(f"Turno: {turno.upper()} | Flechas + Q/E/Z/C (diagonales)")
        if not tiene_queso:
            mostrar_texto("Busca el queso para revelar la meta", 50)
        else:
            mostrar_texto("La meta se ha revelado, ¡llega al final!", 50)

    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if (game_over or victoria) and any(keys):
        pos_gato = random.choice(nodos_ids)
        pos_raton = random.choice([n for n in nodos_ids if n != pos_gato])
        queso = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato)])
        final = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato, queso)])
        tiene_queso = False
        game_over = False
        victoria = False
        turno = "raton"
        inicio = pos_raton