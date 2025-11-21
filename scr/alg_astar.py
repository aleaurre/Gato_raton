from heapq import heappush, heappop

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
    - ocupados: lista de nodos que no se pueden pisar

    Devuelve lista de nodos [inicio, ..., objetivo] o [] si no hay camino.
    """
    if ocupados is None:
        ocupados = []

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

def gato_move_astar(conexiones, nodos_pos, pos_gato, pos_raton):
    """
    Devuelve el SIGUIENTE movimiento del gato usando A*.
    No bloqueamos al ratón como ocupado porque es el objetivo.
    """
    camino = a_star(conexiones, nodos_pos, pos_gato, pos_raton, ocupados=[])
    
    if len(camino) < 2:
        return pos_gato
    
    return camino[1]
