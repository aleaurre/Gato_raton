
from collections import deque
import random
import statistics as st

def vecinos_legales(conexiones, pos_actual, ocupados):
    return [v for v in conexiones[pos_actual] if v not in ocupados]

def bfs_dist(g, s, t):
    if s == t: return 0
    Q, vis, d = deque([s]), {s}, {s: 0}
    while Q:
        u = Q.popleft()
        for v in g[u]:
            if v in vis: continue
            vis.add(v); d[v] = d[u] + 1; Q.append(v)
            if v == t: return d[v]
    return None  

#----------------------------------------------------------------------------------
# Heurísticas 
# Ratón: puntúa cada vecino con score meta y con prob eps hace un paso aleatorio 

def raton_move(conex, pos_g, pos_r, tiene_queso, queso, meta, w_far=1.0, w_goal=1.0, eps=0.0):
    cands = vecinos_legales(conex, pos_r, [pos_g])
    if not cands: return pos_r
    if random.random() < eps:
        return random.choice(cands)

    best, best_score = pos_r, -10**9
    for v in cands:
        dg = bfs_dist(conex, v, pos_g) or 0
        if not tiene_queso:
            dq = bfs_dist(conex, v, queso) or 0
            goal_term = -dq
        else:
            df = bfs_dist(conex, v, meta) or 0
            goal_term = -df
        score = w_far*dg + w_goal*goal_term
        if score > best_score:
            best_score, best = score, v
    return best

# Gato: elegir vecino que más reduzca distancia al ratón (greedy), con probabilidad eps de moverse “al azar” para no caer en ciclos.
def gato_move(conex, pos_g, pos_r, eps=0.0):
    a = vecinos_legales(conex, pos_g, [pos_r])
    if not a: return pos_g
    if random.random() < eps:
        return random.choice(a)
    # elegir el que minimiza distancia al ratón
    a.sort(key=lambda v: bfs_dist(conex, v, pos_r) or 999)
    return a[0]

#----------------------------------------------------------------------------------

def simular_partida(conexiones, pos_g_ini=1, pos_r_ini=0, queso=5, meta=10,
                    pasos_max=120, params_r=None, params_g=None, seed=None):
    if seed is not None: random.seed(seed)
    pos_g, pos_r = pos_g_ini, pos_r_ini
    tiene_queso = False
    turno = "raton"
    pasos = 0
    d_hist = []

    # parámetros por defecto
    if params_r is None: params_r = {"w_far":1.0, "w_goal":1.0, "eps":0.0}
    if params_g is None: params_g = {"eps":0.0}

    while pasos < pasos_max:
        if pos_g == pos_r:  # capturado
            return {"captura":1, "pasos":pasos, "escape":0, "d_prom":(st.mean(d_hist) if d_hist else 0.0)}
        if turno == "raton":
            if not tiene_queso and pos_r == queso: tiene_queso = True
            if tiene_queso and pos_r == meta:
                return {"captura":0, "pasos":pasos, "escape":1, "d_prom":(st.mean(d_hist) if d_hist else 0.0)}

            pos_r = raton_move(conexiones, pos_g, pos_r, tiene_queso, queso, meta,
                               params_r["w_far"], params_r["w_goal"], params_r["eps"])
            turno = "gato"
        else:
            pos_g = gato_move(conexiones, pos_g, pos_r, params_g["eps"])
            turno = "raton"

        d = bfs_dist(conexiones, pos_g, pos_r) or 0
        d_hist.append(d)
        pasos += 1

    return {"captura":0, "pasos":pasos, "escape":1, "d_prom":(st.mean(d_hist) if d_hist else 0.0)}

#----------------------------------------------------------------------------------
# grid search
# Ratón: barremos (w_far, w_goal, eps) y elegimos lo que maximiza tasa de escape

def entrenar_raton(conexiones, episodios=400, semillas=(0,1,2,3),
                   w_far_vals=(0.5,1.0,1.5,2.0),
                   w_goal_vals=(0.5,1.0,1.5,2.0),
                   eps_vals=(0.0,0.05,0.1),
                   pos_g_ini=1, pos_r_ini=0, queso=5, meta=10):
    mejor = None
    best_score = -1
    for wf in w_far_vals:
        for wg in w_goal_vals:
            for eps in eps_vals:
                caps, escs = 0, 0
                pasos_list, d_list = [], []
                for s in semillas:
                    for ep in range(episodios//len(semillas)):
                        r = simular_partida(conexiones, pos_g_ini, pos_r_ini, queso, meta,
                                            params_r={"w_far":wf,"w_goal":wg,"eps":eps},
                                            params_g={"eps":0.05}, seed=(1000*s+ep))
                        caps += r["captura"]; escs += r["escape"]
                        pasos_list.append(r["pasos"]); d_list.append(r["d_prom"])
                tasa_escape = escs / (caps+escs)
                # criterio: priorizar mayor tasa de escape y de desempate más distancia promedio
                score = (tasa_escape, st.mean(d_list))
                if score > best_score:
                    best_score = score
                    mejor = {"w_far":wf, "w_goal":wg, "eps":eps, "tasa_escape":tasa_escape,
                             "pasos_prom":st.mean(pasos_list), "d_prom":st.mean(d_list)}
    return mejor


# Gato: barremos eps y nos quedamos con el que más captura y en menos pasos
def entrenar_gato(conexiones, episodios=400, semillas=(0,1,2,3), eps_vals=(0.0,0.05,0.1,0.15),
                  pos_g_ini=1, pos_r_ini=0, queso=5, meta=10):
    mejor = None
    best_tuple = (-1, 1e9)  
    for eps in eps_vals:
        caps, escs = 0, 0
        pasos_list, d_list = [], []
        for s in semillas:
            for ep in range(episodios//len(semillas)):
                r = simular_partida(conexiones, pos_g_ini, pos_r_ini, queso, meta,
                                    params_r={"w_far":1.5,"w_goal":1.5,"eps":0.05},
                                    params_g={"eps":eps}, seed=(2000*s+ep))
                caps += r["captura"]; escs += r["escape"]
                pasos_list.append(r["pasos"]); d_list.append(r["d_prom"])
        tasa_cap = caps / (caps+escs)
        crit = (tasa_cap, -st.mean(pasos_list))
        if crit > best_tuple:
            best_tuple = crit
            mejor = {"eps":eps, "tasa_captura":tasa_cap, "pasos_prom":st.mean(pasos_list), "d_prom":st.mean(d_list)}
    return mejor


