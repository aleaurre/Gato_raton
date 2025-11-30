"""
experiments_runner.py

Script to run the battery of experiments requested by the user.

It executes the six pairings:
 1) G_random vs R_astar
 2) G_astar  vs R_random
 3) G_minmax vs R_astar
 4) G_random vs R_minmax
 5) G_astar  vs R_minmax
 6) G_minmax vs R_random

For each pairing it runs N_SEEDS (default 20) games, records:
 - winner ("gato","raton","empate")
 - pasos (turns until end)
 - tiempo (wall-clock seconds of the simulation loop)

Outputs:
 - CSV with raw results (results_raw.csv)
 - Summary table (results_summary.csv)
 - Two PNG plots: win_rates.png and avg_duration.png

How to run:
    python -m scr.experiments_runner

Requirements: pandas, matplotlib

"""

import random
import time
import statistics as st
from collections import Counter
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Choose map: import config_small or config_big
from scr.config_small import conexiones, nodos
# from scr.config_big import conexiones, nodos

# Algorithms
from scr.alg.alg_astar import gato_move_astar, raton_move_astar
from scr.alg.alg_minimax import gato_move_minimax, raton_move_minimax
from scr.alg.alg_random import gato_move_random, raton_move_random

# ------------------------------------------------------------------
# Utility: choose movement function given mode string
# ------------------------------------------------------------------

def mover_gato(mode, pos_g, pos_r, conexiones, nodos):
    if mode == "astar":
        return gato_move_astar(conexiones, nodos, pos_g, pos_r)
    elif mode == "minimax":
        return gato_move_minimax(conexiones, nodos, pos_g, pos_r)
    elif mode == "random":
        return gato_move_random(conexiones, pos_g, pos_r)
    else:
        raise ValueError(f"Modo gato desconocido: {mode}")


def mover_raton(mode, pos_g, pos_r, queso, final, tiene_queso, conexiones, nodos):
    if mode == "astar":
        return raton_move_astar(conexiones, nodos, pos_g, pos_r, queso, final, tiene_queso)
    elif mode == "minimax":
        # minimax implementation ignores queso/meta in this project
        return raton_move_minimax(conexiones, nodos, pos_g, pos_r)
    elif mode == "random":
        return raton_move_random(conexiones, pos_g, pos_r)
    else:
        raise ValueError(f"Modo raton desconocido: {mode}")


# ------------------------------------------------------------------
# Simulate one game using the selected modes
# ------------------------------------------------------------------

def simular_un_juego(mode_gato, mode_raton, conexiones, nodos, max_pasos=200, seed=None):
    """
    Simula una partida completa y devuelve dict con keys:
      - 'winner': 'gato'|'raton'|'empate'
      - 'pasos': int (número de turnos)
      - 'duration': float (tiempo en segundos de la simulación)
    """
    if seed is not None:
        random.seed(seed)

    nodos_ids = list(nodos.keys())
    pos_raton = random.choice(nodos_ids)
    pos_gato  = random.choice([n for n in nodos_ids if n != pos_raton])
    queso     = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato)])
    final     = random.choice([n for n in nodos_ids if n not in (pos_raton, pos_gato, queso)])

    tiene_queso = False
    turno = "raton"

    pasos = 0

    t0 = time.perf_counter()

    while pasos < max_pasos:
        if turno == "raton":
            pos_raton = mover_raton(mode_raton, pos_gato, pos_raton, queso, final, tiene_queso, conexiones, nodos)
            # raton picks up cheese
            if not tiene_queso and pos_raton == queso:
                tiene_queso = True
            turno = "gato"
        else:
            pos_gato = mover_gato(mode_gato, pos_gato, pos_raton, conexiones, nodos)
            turno = "raton"

        pasos += 1

        # Check terminal conditions
        if pos_gato == pos_raton:
            duration = time.perf_counter() - t0
            return {"winner": "gato", "pasos": pasos, "duration": duration}

        if tiene_queso and pos_raton == final:
            duration = time.perf_counter() - t0
            return {"winner": "raton", "pasos": pasos, "duration": duration}

    duration = time.perf_counter() - t0
    return {"winner": "empate", "pasos": pasos, "duration": duration}


# ------------------------------------------------------------------
# Experiment runner for a given pairing
# ------------------------------------------------------------------

def run_experiments(pair_label, mode_gato, mode_raton, repetitions=20, seed_base=0, max_pasos=200):
    results = []
    for i in range(repetitions):
        seed = seed_base + i
        out = simular_un_juego(mode_gato, mode_raton, conexiones, nodos, max_pasos=max_pasos, seed=seed)
        out["pair"] = pair_label
        out["mode_gato"] = mode_gato
        out["mode_raton"] = mode_raton
        out["seed"] = seed
        results.append(out)
    return results


# ------------------------------------------------------------------
# Main: run all six pairings and save results, compute summary and plots
# ------------------------------------------------------------------

def main():
    PAIRINGS = [
        ("G_random vs R_astar", "random", "astar"),
        ("G_astar vs R_random", "astar", "random"),
        ("G_minmax vs R_astar", "minimax", "astar"),
        ("G_random vs R_minmax", "random", "minimax"),
        ("G_astar vs R_minmax", "astar", "minimax"),
        ("G_minmax vs R_random", "minimax", "random"),
    ]

    REPETITIONS = 20
    all_results = []

    print("Iniciando experiments: each pairing -> {} games".format(REPETITIONS))

    for idx, (label, mg, mr) in enumerate(PAIRINGS):
        print(f"Running pairing {idx+1}/{len(PAIRINGS)}: {label}")
        res = run_experiments(label, mg, mr, repetitions=REPETITIONS, seed_base=1000*idx)
        all_results.extend(res)

    df = pd.DataFrame(all_results)
    out_dir = Path("experiment_results")
    out_dir.mkdir(exist_ok=True)

    raw_csv = out_dir / "results_raw.csv"
    df.to_csv(raw_csv, index=False)
    print(f"Raw results saved to {raw_csv}")

    # Summary per pairing
    summary_rows = []
    for label, group in df.groupby("pair"):
        winners = Counter(group["winner"])
        total = len(group)
        tasa_gato = winners.get("gato", 0) / total
        tasa_raton = winners.get("raton", 0) / total
        tasa_empate = winners.get("empate", 0) / total
        pasos_prom = group["pasos"].mean()
        dur_prom = group["duration"].mean()
        dur_med = group["duration"].median()
        dur_std = group["duration"].std()

        summary_rows.append({
            "pair": label,
            "mode_gato": group.iloc[0]["mode_gato"],
            "mode_raton": group.iloc[0]["mode_raton"],
            "repetitions": total,
            "gato_wins": winners.get("gato", 0),
            "raton_wins": winners.get("raton", 0),
            "empates": winners.get("empate", 0),
            "tasa_gato": tasa_gato,
            "tasa_raton": tasa_raton,
            "tasa_empate": tasa_empate,
            "pasos_prom": pasos_prom,
            "dur_prom": dur_prom,
            "dur_med": dur_med,
            "dur_std": dur_std,
        })

    df_summary = pd.DataFrame(summary_rows)
    summary_csv = out_dir / "results_summary.csv"
    df_summary.to_csv(summary_csv, index=False)
    print(f"Summary saved to {summary_csv}")

    # Plots
    # 1) Win rates (gato vs raton vs empate) per pairing (stacked bar)
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = df_summary["pair"].tolist()
    gato_rates = df_summary["tasa_gato"].tolist()
    raton_rates = df_summary["tasa_raton"].tolist()
    empate_rates = df_summary["tasa_empate"].tolist()

    x = range(len(labels))
    ax.bar(x, gato_rates, label="Gato")
    ax.bar(x, raton_rates, bottom=gato_rates, label="Ratón")
    bottom2 = [g + r for g, r in zip(gato_rates, raton_rates)]
    ax.bar(x, empate_rates, bottom=bottom2, label="Empate")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Tasa")
    ax.set_title("Win rates por pairing")
    ax.legend()
    plt.tight_layout()
    winrates_png = out_dir / "win_rates.png"
    fig.savefig(winrates_png)
    print(f"Win rates plot saved to {winrates_png}")

    # 2) Average duration per pairing (seconds)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(labels, df_summary["dur_prom"].tolist())
    ax2.set_xticklabels(labels, rotation=30, ha="right")
    ax2.set_ylabel("Duración promedio (s)")
    ax2.set_title("Duración promedio de las partidas por pairing")
    plt.tight_layout()
    dur_png = out_dir / "avg_duration.png"
    fig2.savefig(dur_png)
    print(f"Average duration plot saved to {dur_png}")

    print("Experiments finished. Revisa la carpeta 'experiment_results' para los CSV y PNG.")


if __name__ == "__main__":
    main()