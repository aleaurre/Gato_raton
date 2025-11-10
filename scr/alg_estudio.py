"""

Módulo para el "análisis del mapa" del proyecto Gato y Ratón.
Tiene funciones generales que: calculan caminos mínimos, matriz
(de diccionario) de distancias, comprobación de conectividad, detección
de cuellos de botella (puntos de articulación) y nodos más centrales.

Uso: importarlo desde el fichero principal del juego y pasarle las
estructuras `conexiones` y `nodos` ya definidas.

"""

from collections import deque, defaultdict
from typing import Dict, List, Tuple, Set, Any


# Types a usar
Nodo = int
Grafo = Dict[Nodo, List[Nodo]]
PosDict = Dict[Nodo, Tuple[int, int]]


# Funciones básicas grafo
def bfs_shortest_path(grafo: Grafo, origen: Nodo, destino: Nodo) -> Tuple[List[Nodo], int]:
    """
    Esta función es:BFS que devuelve el camino más corto (lista de nodos) entre origen y destino
    en un grafo no ponderado, y la distancia (nº de aristas).

    Si no existe camino devuelve ([], -1).
    """
    # Cola para BFS: cada elemento es (nodo_actual)
    if origen == destino:
        return [origen], 0

    visitado: Set[Nodo] = set()
    padre: Dict[Nodo, Nodo] = {}
    q = deque()
    q.append(origen)
    visitado.add(origen)

    while q:
        u = q.popleft()
        for v in grafo.get(u, []):
            if v not in visitado:
                visitado.add(v)
                padre[v] = u
                if v == destino:
                    # reconstruir camino
                    camino = [v]
                    while camino[-1] != origen:
                        camino.append(padre[camino[-1]])
                    camino.reverse()
                    return camino, len(camino) - 1
                q.append(v)

    return [], -1


def all_pairs_shortest_paths(grafo: Grafo) -> Dict[Nodo, Dict[Nodo, int]]:
    """
    Calcula distancias mínimas entre todos los pares de nodos usando BFS
    desde cada nodo (suficiente cuando los arcos tienen peso uniforme).

    Devuelve un diccionario dist[origen][destino] = distancia (int) o -1 si no hay camino.
    """
    dist: Dict[Nodo, Dict[Nodo, int]] = {}
    for s in grafo.keys():
        # BFS desde s
        distancia_s: Dict[Nodo, int] = {n: -1 for n in grafo.keys()}
        q = deque()
        q.append(s)
        distancia_s[s] = 0
        while q:
            u = q.popleft()
            for v in grafo.get(u, []):
                if distancia_s[v] == -1:
                    distancia_s[v] = distancia_s[u] + 1
                    q.append(v)
        dist[s] = distancia_s
    return dist


def is_connected(grafo: Grafo) -> bool:
    """
    Comprueba si el grafo está conectado/conexo, es decir, si desde cualquier nodo se llega a todos
    """
    if not grafo:
        return True
    inicio = next(iter(grafo))
    visitado: Set[Nodo] = set()
    q = deque([inicio])
    visitado.add(inicio)
    while q:
        u = q.popleft()
        for v in grafo.get(u, []):
            if v not in visitado:
                visitado.add(v)
                q.append(v)
    return len(visitado) == len(grafo)


# Detección de cuellos de botella (puntos de articulación)


def articulation_points(grafo: Grafo) -> Set[Nodo]:
    """
    Determina los puntos de articulación (cut vertices) del grafo mediante
    un algoritmo DFS. 
    Un punto de articulación es un nodo cuya eliminación aumenta el número de componentes conectadas: son 'cuellos de botella'.

    Devuelve un set con los nodos críticos.
    """
    time = 0
    visited: Set[Nodo] = set()
    disc: Dict[Nodo, int] = {}
    low: Dict[Nodo, int] = {}
    parent: Dict[Nodo, Any] = {}
    ap: Set[Nodo] = set()

    # defino la función dfs dentro
    def dfs(u: Nodo):
        nonlocal time
        visited.add(u)
        disc[u] = time
        low[u] = time
        time += 1
        children = 0

        for v in grafo.get(u, []):
            if v not in visited:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                # caso 1: u es root y tiene dos o más hijos
                if u not in parent and children > 1:
                    ap.add(u)
                # caso 2: u no es root y low[v] >= disc[u]
                if u in parent and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u, None):
                low[u] = min(low[u], disc[v])

    for node in grafo.keys():
        if node not in visited:
            dfs(node)
    return ap


# Centralidad simple (grado: numero de vecinos)
def degree_centrality(grafo: Grafo) -> Dict[Nodo, int]:
    """
    Calcula la centralidad por grado (num de vecinos).
    Devuelve dict nodo -> grado.
    """
    return {n: len(neis) for n, neis in grafo.items()}



# FUNCIÓN DE ANÁLISIS GLOBAL ( incorpora todo )
def analyze_map(grafo: Grafo,
                nodos_pos: PosDict,
                pos_gato: Nodo,
                pos_raton: Nodo,
                queso: Nodo,
                final: Nodo = None,
                verbose: bool = True) -> Dict[str, Any]:
    """
    Función principal que ejecuta el conjunto de análisis

    Parámetros:
      - grafo: dict de adyacencia
      - nodos_pos: posiciones (x,y) de cada nodo (solo para visualizaciones opcionales)
      - pos_gato: nodo inicial del gato
      - pos_raton: nodo inicial del ratón
      - queso: nodo donde está el queso
      - final: nodo de meta (opcional)
      - verbose: si True imprime un resumen por consola

    Retorna un diccionario con:
      - 'camino_raton_queso': (camino, distancia)
      - 'camino_gato_raton': (camino, distancia)
      - 'distancias': matriz (dict de dicts) con todas las distancias
      - 'conexo': boolean
      - 'articulation_points': set de nodos críticos
      - 'degree_centrality': dict nodo->grado
      - 'nodo_mas_central': nodo con mayor grado
    """
    resultados: Dict[str, Any] = {}

    # 1) Camino más corto ratón -> queso
    camino_rq, dist_rq = bfs_shortest_path(grafo, pos_raton, queso)
    resultados['camino_raton_queso'] = (camino_rq, dist_rq)

    # 2) Camino más corto gato -> ratón
    camino_gr, dist_gr = bfs_shortest_path(grafo, pos_gato, pos_raton)
    resultados['camino_gato_raton'] = (camino_gr, dist_gr)

    # 3) Matriz/diccionario de distancias entre todos los nodos
    dist_all = all_pairs_shortest_paths(grafo)
    resultados['distancias'] = dist_all

    # 4) Analisis de conectividad
    conex = is_connected(grafo)
    resultados['conexo'] = conex

    # 5) Detección de cuellos de botella (puntos de articulación)
    ap = articulation_points(grafo)
    resultados['articulation_points'] = ap

    # 6) Mejor nodo por grado (centralidad simple)
    deg = degree_centrality(grafo)
    resultados['degree_centrality'] = deg

    # encontrar nodo con mayor grado (si hay empates devuelve uno cualquiera)
    nodo_mas = max(deg.items(), key=lambda kv: kv[1])[0] if deg else None
    resultados['nodo_mas_central'] = nodo_mas

    # Mensajes resumidos si verbose ( solo si es True se imprime este mensaje en la terminal )
    if verbose:
        print("--- Resumen del análisis del mapa ---")
        print(f"Camino ratón -> queso: {camino_rq} (distancia {dist_rq})")
        print(f"Camino gato -> ratón: {camino_gr} (distancia {dist_gr})")
        print("Conectividad del grafo:", "Conexo" if conex else "No conexo")
        print("Puntos de articulación (cuellos de botella):", ap)
        print("Grado (centralidad) por nodo:")
        for n, d in sorted(deg.items()):
            print(f"  Nodo {n}: grado {d}")
        print(f"Nodo con mayor grado: {nodo_mas}")
        print("--- Fin del resumen ---")

    return resultados




