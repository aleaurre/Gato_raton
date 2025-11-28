# scr/alg_minimax.py

from math import inf
from scr.alg.alg_entrenamiento import bfs_dist


# Funciones auxiliares

def vecinos_legales(conexiones, pos, ocupados=None):
    """
    Devuelve vecinos evitando nodos en 'ocupados'.
    Si no hay vecinos válidos, se queda en su lugar.
    """
    if ocupados is None:
        ocupados = set()
    vecinos = [v for v in conexiones[pos] if v not in ocupados]
    return vecinos if vecinos else [pos]


# Función de evaluación generalizada

def evaluar_estado_general(conexiones, pos_gato, pos_raton, max_agent):
    """
    Evalúa un estado dependiendo de quién sea MAX.
    
    max_agent = 'gato'  → el gato quiere atrapar al ratón.
    max_agent = 'raton' → el ratón quiere alejarse del gato y acercarse a queso/meta.
    
    NOTA: en esta versión no incluimos queso/meta (porque depende del motor),
    pero dejamos el hook preparado por si lo quieren ampliar.
    """

    # Caso terminal: captura
    if pos_gato == pos_raton:
        if max_agent == "gato":
            return +10_000   # excelente para el gato
        else:
            return -10_000   # pésimo para el ratón

    # Distancia gato-ratón
    d = bfs_dist(conexiones, pos_gato, pos_raton)

    if d is None:
        # Si no hay camino: posición horrible para el gato
        # pero muy buena para el ratón
        return -10_000 if max_agent == "gato" else +10_000

    # max_agent = gato → quiere d chica (acercarse)
    # max_agent = raton → quiere d grande (alejarse)
    if max_agent == "gato":
        return -d  # d chica → valor grande
    else:
        return +d  # d grande → valor grande


# Minimax generalizado con poda alfa–beta

def minimax_gen(conexiones,
                pos_gato,
                pos_raton,
                profundidad,
                turno_agente,
                max_agent,
                alpha=-inf,
                beta=inf):
    """
    minimax_gen → versión generalizada.

    Parámetros:
    - turno_agente : 'gato' o 'raton' (quién mueve ahora)
    - max_agent    : 'gato' o 'raton' (quién es el jugador MAX)
    """

    # Caso terminal: captura
    if pos_gato == pos_raton:
        valor = evaluar_estado_general(conexiones, pos_gato, pos_raton, max_agent)
        return valor, pos_gato if turno_agente == "gato" else pos_raton

    # Profundidad límite
    if profundidad == 0:
        valor = evaluar_estado_general(conexiones, pos_gato, pos_raton, max_agent)
        return valor, pos_gato if turno_agente == "gato" else pos_raton

    # ¿Quién es MAX y quién es MIN?
    es_max = (turno_agente == max_agent)

    # Turno del gato
    if turno_agente == "gato":
        mejor_val = -inf if es_max else inf
        mejor_mov = pos_gato

        for mov in vecinos_legales(conexiones, pos_gato, ocupados={pos_raton}):
            val, _ = minimax_gen(
                conexiones,
                pos_gato=mov,
                pos_raton=pos_raton,
                profundidad=profundidad - 1,
                turno_agente="raton",
                max_agent=max_agent,
                alpha=alpha,
                beta=beta
            )

            if es_max:
                if val > mejor_val:
                    mejor_val = val
                    mejor_mov = mov
                alpha = max(alpha, mejor_val)
            else:
                if val < mejor_val:
                    mejor_val = val
                    mejor_mov = mov
                beta = min(beta, mejor_val)

            if beta <= alpha:
                break  # poda

        return mejor_val, mejor_mov

    # Turno del ratón
    else:  # turno_agente == "raton"
        mejor_val = -inf if es_max else inf
        mejor_mov = pos_raton

        for mov in vecinos_legales(conexiones, pos_raton, ocupados={pos_gato}):
            val, _ = minimax_gen(
                conexiones,
                pos_gato=pos_gato,
                pos_raton=mov,
                profundidad=profundidad - 1,
                turno_agente="gato",
                max_agent=max_agent,
                alpha=alpha,
                beta=beta
            )

            if es_max:
                if val > mejor_val:
                    mejor_val = val
                    mejor_mov = mov
                alpha = max(alpha, mejor_val)
            else:
                if val < mejor_val:
                    mejor_val = val
                    mejor_mov = mov
                beta = min(beta, mejor_val)

            if beta <= alpha:
                break  # poda

        return mejor_val, mejor_mov


# Interfaces públicas para movimiento del gato o del ratón

def gato_move_minimax(conexiones, nodos_pos, pos_gato, pos_raton, profundidad=3):
    """
    Movimiento del gato usando Minimax:
    - El gato es MAX
    - El ratón es MIN
    """
    _, mov = minimax_gen(
        conexiones,
        pos_gato=pos_gato,
        pos_raton=pos_raton,
        profundidad=profundidad,
        turno_agente="gato",
        max_agent="gato"
    )
    return mov


def raton_move_minimax(conexiones, nodos_pos, pos_gato, pos_raton, profundidad=3):
    """
    Movimiento del ratón usando Minimax:
    - El ratón es MAX
    - El gato es MIN
    """
    _, mov = minimax_gen(
        conexiones,
        pos_gato=pos_gato,
        pos_raton=pos_raton,
        profundidad=profundidad,
        turno_agente="raton",
        max_agent="raton"
    )
    return mov