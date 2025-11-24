# scr/alg_astar.py

from heapq import heappush, heappop


# Heurística y A* genérico

def heuristica(nodos_pos, a, b):
    """
    Heurística Manhattan entre dos nodos, usando sus posiciones (x, y).
    """
    (x1, y1) = nodos_pos[a]
    (x2, y2) = nodos_pos[b]
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(conexiones, nodos_pos, inicio, objetivo, ocupados=None):
    """
    A* clásico en grafo no ponderado.
    - conexiones: dict nodo -> lista de vecinos
    - nodos_pos: dict nodo -> (x,y)
    - inicio, objetivo: nodos
    - ocupados: colección de nodos que NO se pueden pisar,
      excepto el objetivo (lo permitimos para poder capturar / llegar).

    Devuelve lista de nodos [inicio, ..., objetivo] o [] si no hay camino.
    """
    if ocupados is None:
        ocupados = set()
    else:
        ocupados = set(ocupados)

    # Nunca bloquear el objetivo:
    if objetivo in ocupados:
        ocupados.remove(objetivo)

    if inicio == objetivo:
        return [inicio]

    heap = []
    heappush(heap, (0, inicio))

    g = {inicio: 0}
    padre = {inicio: None}
    visitado = set()

    while heap:
        f_actual, actual = heappop(heap)

        if actual == objetivo:
            # reconstruir camino
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1]

        if actual in visitado:
            continue
        visitado.add(actual)

        for vecino in conexiones[actual]:
            if vecino in ocupados:
                continue

            nuevo_g = g[actual] + 1  # todas las aristas pesan 1
            if vecino not in g or nuevo_g < g[vecino]:
                g[vecino] = nuevo_g
                f = nuevo_g + heuristica(nodos_pos, vecino, objetivo)
                heappush(heap, (f, vecino))
                padre[vecino] = actual

    return []  # no hay camino


# Movimiento genérico usando A* hacia un objetivo

def agent_move_astar_to_target(conexiones, nodos_pos,
                               pos_agente, objetivo,
                               ocupados=None):
    """
    Devuelve el SIGUIENTE movimiento de un agente hacia 'objetivo'
    usando A*.

    - ocupados: nodos que el agente NO puede pisar (obstáculos, oponente, etc.),
      pero el 'objetivo' nunca se bloquea.
    """
    camino = a_star(conexiones, nodos_pos, pos_agente, objetivo, ocupados=ocupados)

    if len(camino) < 2:
        # No hay camino útil o ya está en el objetivo
        return pos_agente

    # Siguiente nodo del camino
    return camino[1]


# Movimiento del GATO con A*

def gato_move_astar(conexiones, nodos_pos, pos_gato, pos_raton):
    """
    Movimiento del gato usando A*.
    Objetivo: el ratón.
    No bloqueamos al ratón como 'ocupado' porque es justamente el objetivo.
    """
    return agent_move_astar_to_target(
        conexiones,
        nodos_pos,
        pos_agente=pos_gato,
        objetivo=pos_raton,
        ocupados=[]  # puede pisar al ratón para capturarlo
    )


# Movimiento del RATÓN con A*

def raton_move_astar(conexiones, nodos_pos,
                     pos_gato, pos_raton,
                     queso, meta, tiene_queso):
    """
    Movimiento del ratón usando A*.

    - Si NO tiene queso: objetivo = queso.
    - Si YA tiene queso: objetivo = meta.

    En ambos casos, el ratón intenta evitar pisar al gato,
    por lo que el gato se pasa en 'ocupados'.
    """
    if not tiene_queso:
        objetivo = queso
    else:
        objetivo = meta

    return agent_move_astar_to_target(
        conexiones,
        nodos_pos,
        pos_agente=pos_raton,
        objetivo=objetivo,
        ocupados={pos_gato}  # evitamos pisar al gato
    )