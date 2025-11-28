from config_small import conexiones, nodos
from scr.alg.alg_astar import a_star, gato_move_astar

print("Ejecutando test_astar...")

inicio = 0
objetivo = 10  # por ejemplo, el nodo de la derecha del todo en el mapa chico

camino = a_star(conexiones, nodos, inicio, objetivo)
print("Camino óptimo 0 -> 10:", camino)

siguiente = gato_move_astar(conexiones, nodos, inicio, objetivo)
print("Siguiente movimiento del gato:", siguiente)