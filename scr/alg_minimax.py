# scr/alg_minimax.py

from math import inf
from scr.alg_entrenamiento import bfs_dist


def vecinos_legales(conexiones, pos, ocupados=None):
    """
    Vecinos del nodo 'pos' excluyendo los nodos en 'ocupados'.
    Si no hay vecinos válidos, el agente se queda donde está.
    """
    if ocupados is None:
        ocupados = set()
    return [v for v in conexiones[pos] if v not in ocupados] or [pos]


def evaluar_estado(conexiones, pos_gato, pos_raton):
    """
    Función de evaluación para Minimax.
    Valores grandes => buenos para el gato.
    Criterio simple:
      - Si el gato atrapó al ratón: valor altísimo
      - Si no, cuanto más cerca esté el gato, mejor.
    """
    if pos_gato == pos_raton:
        return 10_000  # estado terminal: captura

    d = bfs_dist(conexiones, pos_gato, pos_raton)
    if d is None:
        # Si no hay camino, penalizamos fuerte (el gato está perdido)
        return -10_000

    # Mientras más chico d, mejor para el gato.
    # Usamos el negativo para que d chico => valor grande.
    return -d


def minimax(conexiones, pos_gato, pos_raton, profundidad, es_turno_gato,
            alpha=-inf, beta=inf):
    """
    Minimax con poda alfa-beta.
    - conexiones: grafo (dict nodo -> lista de vecinos)
    - pos_gato, pos_raton: posiciones actuales
    - profundidad: profundidad máxima del árbol
    - es_turno_gato: True si juega el gato (MAX), False si juega el ratón (MIN)
    """

    # Estado terminal: gato atrapa
    if pos_gato == pos_raton:
        return evaluar_estado(conexiones, pos_gato, pos_raton), pos_gato

    # O alcanzamos la profundidad máxima
    if profundidad == 0:
        return evaluar_estado(conexiones, pos_gato, pos_raton), pos_gato

    if es_turno_gato:
        # MAX: el gato quiere maximizar la evaluación
        mejor_valor = -inf
        mejor_mov = pos_gato

        # El gato puede moverse a cualquier vecino (incluyendo el ratón = captura)
        for siguiente in vecinos_legales(conexiones, pos_gato):
            valor, _ = minimax(
                conexiones,
                pos_gato=siguiente,
                pos_raton=pos_raton,
                profundidad=profundidad - 1,
                es_turno_gato=False,
                alpha=alpha,
                beta=beta
            )

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = siguiente

            alpha = max(alpha, mejor_valor)
            if beta <= alpha:
                break  # poda beta

        return mejor_valor, mejor_mov

    else:
        # MIN: el ratón quiere minimizar la evaluación (escapar del gato)
        peor_valor = inf
        peor_mov = pos_raton

        # El ratón intenta no pisar el nodo del gato
        for siguiente in vecinos_legales(conexiones, pos_raton, ocupados={pos_gato}):
            valor, _ = minimax(
                conexiones,
                pos_gato=pos_gato,
                pos_raton=siguiente,
                profundidad=profundidad - 1,
                es_turno_gato=True,
                alpha=alpha,
                beta=beta
            )

            if valor < peor_valor:
                peor_valor = valor
                peor_mov = siguiente

            beta = min(beta, peor_valor)
            if beta <= alpha:
                break  # poda alfa

        return peor_valor, peor_mov


def gato_move_minimax(conexiones, nodos_pos, pos_gato, pos_raton, profundidad=3):
    """
    Decide el movimiento del gato usando Minimax con poda alfa-beta.
    - conexiones: grafo
    - nodos_pos: no lo usamos por ahora, pero lo dejamos para compatibilidad con A*
    - pos_gato: posición actual del gato
    - pos_raton: posición actual del ratón
    - profundidad: profundidad de búsqueda (2–3 está bien para 11 nodos)
    """
    # Si ya está sobre el ratón, no hace falta moverse
    if pos_gato == pos_raton:
        return pos_gato

    _, mejor_mov = minimax(
        conexiones,
        pos_gato=pos_gato,
        pos_raton=pos_raton,
        profundidad=profundidad,
        es_turno_gato=True
    )
    return mejor_mov