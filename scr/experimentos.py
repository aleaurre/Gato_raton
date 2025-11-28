# # python -m scr.experimentos

import random
from time import sleep

# Mapa (podés cambiar a config_big)
from scr.config_small import conexiones, nodos

# Algoritmos
from scr.alg_astar import gato_move_astar, raton_move_astar  
from scr.alg_minimax import gato_move_minimax, raton_move_minimax  
from scr.alg_random import gato_move_random, raton_move_random  


# ============= CONFIGURAR QUÉ ALGORITMO USA CADA AGENTE =============
MODO_GATO  = "astar"    # opciones: astar / minimax / random
MODO_RATON = "minimax"  # opciones: astar / minimax / random
# ===================================================================


def elegir_movimiento_gato(pos_gato, pos_raton):
    if MODO_GATO == "astar":
        return gato_move_astar(conexiones, nodos, pos_gato, pos_raton)
    elif MODO_GATO == "minimax":
        return gato_move_minimax(conexiones, nodos, pos_gato, pos_raton)
    return gato_move_random(conexiones, pos_gato, pos_raton)


def elegir_movimiento_raton(pos_gato, pos_raton, queso, final, tiene_queso):
    if MODO_RATON == "astar":
        return raton_move_astar(conexiones, nodos, pos_gato, pos_raton, queso, final, tiene_queso)
    elif MODO_RATON == "minimax":
        return raton_move_minimax(conexiones, nodos, pos_gato, pos_raton)
    return raton_move_random(conexiones, pos_gato, pos_raton)


def ejecutar_partida(max_pasos=100):
    nodos_ids = list(nodos.keys())

    # Estado inicial
    pos_raton = random.choice(nodos_ids)
    pos_gato  = random.choice([n for n in nodos_ids if n != pos_raton])
    queso     = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato)])
    final     = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato, queso)])

    tiene_queso = False
    turno = "raton"

    print("\n====== INICIO DE PARTIDA ======")
    print(f"Gato:   {MODO_GATO}  |  Pos: {pos_gato}")
    print(f"Ratón:  {MODO_RATON} |  Pos: {pos_raton}")
    print(f"Queso:  {queso}  | Final: {final}")
    print("================================")

    for paso in range(max_pasos):

        print(f"\n--- Paso {paso} | Turno: {turno} ---")
        
        if turno == "raton":
            pos_raton = elegir_movimiento_raton(pos_gato, pos_raton, queso, final, tiene_queso)
            turno = "gato"
        else:
            pos_gato = elegir_movimiento_gato(pos_gato, pos_raton)
            turno = "raton"

        print(f"Pos Gato: {pos_gato} | Pos Ratón: {pos_raton}")

        # Captura
        if pos_gato == pos_raton:
            print("❌ ¡El gato atrapó al ratón! GAME OVER")
            return

        # Ratón toma el queso
        if pos_raton == queso and not tiene_queso:
            tiene_queso = True
            print("🧀 El ratón consiguió el queso!")

        # Ratón gana
        if pos_raton == final and tiene_queso:
            print("🏁 ¡El ratón llegó a la meta con el queso! VICTORIA")
            return

        sleep(0.6)

    print("⏳ Se acabaron los pasos → Empate")


if __name__ == "__main__":
    ejecutar_partida()
