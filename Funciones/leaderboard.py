import json
from operator import getitem


def guardar_partida(jugador):
    try:
        leaderboard = open("Archivos/leaderboard", "r", encoding="utf-8")
        partidas = json.load(leaderboard)
        leaderboard.close()
        partidas[str(len(partidas) + 1)] = jugador

        partidas = dict(sorted(partidas.items(), reverse=True,
                               key=lambda x: getitem(x[1], 'puntaje')))

        leaderboard = open("Archivos/leaderboard", "w", encoding="utf-8")
        json.dump(partidas, leaderboard, ensure_ascii=False, indent=4)
        leaderboard.close()
    except FileNotFoundError:
        leaderboard = open("Archivos/leaderboard", "w", encoding="utf-8")
        partidas = {}
        partidas[str(len(partidas) + 1)] = jugador
        json.dump(partidas, leaderboard, ensure_ascii=False, indent=4)
        leaderboard.close()
