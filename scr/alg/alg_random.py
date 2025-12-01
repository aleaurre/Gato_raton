# scr/alg_random.py

import random
from scr.alg.funcs_base import bfs_dist  # no es necesario pero lo dejamos por consistencia


def vecinos_legales(conexiones, pos, ocupados=None):
    """
    Devuelve los vecinos legales del agente.
    'ocupados' es un set con nodos donde NO se puede mover (como el oponente).
    """
    if ocupados is None:
        ocupados = set()
    vecinos = [v for v in conexiones[pos] if v not in ocupados]
    return vecinos if vecinos else [pos]


# Movimiento Random para ambos agentes

def agent_move_random(conexiones, pos_agente, pos_oponente):
    """
    Movimiento aleatorio para cualquier agente (gato o ratón).

    - Elige un vecino al azar.
    - Evita pisar al otro agente.
    """

    vecinos = vecinos_legales(conexiones, pos_agente, ocupados={pos_oponente})
    
    # random.choice siempre elige uno; si no hay vecinos válidos,
    # vecinos_legales ya devolvió [pos_agente]
    return random.choice(vecinos)


# Interfaces específicas para gato y ratón (por claridad)

def gato_move_random(conexiones, pos_gato, pos_raton):
    return agent_move_random(conexiones, pos_gato, pos_raton)


def raton_move_random(conexiones, pos_gato, pos_raton):
    return agent_move_random(conexiones, pos_raton, pos_gato)
