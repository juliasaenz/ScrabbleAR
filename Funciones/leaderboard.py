import json
from operator import getitem


def guardar_partida(jugador):
    try:
        leaderboard = open("Archivos/leaderboard", "r", encoding="utf-8")
        partidas = json.load(leaderboard)
        leaderboard.close()
        clave = jugador['nombre']
        i = 0

        while clave in partidas.keys():
            clave = jugador['nombre'] + str(i)
            i = i + 1

        print("esta es la clave: ",clave)
        partidas[clave] = jugador

        partidas = dict(sorted(partidas.items(), reverse=True,
                               key=lambda x: getitem(x[1], 'puntaje')))

        if len(partidas) > 10:
            print("aca tengo que sacar a alguno")
            min_p = 9999
            min_c = 9999
            for clave, datos in partidas.items():
                if datos['puntaje'] < min_p:
                    min_p = datos['puntaje']
                    min_c = clave
            del partidas[min_c]

        leaderboard = open("Archivos/leaderboard", "w", encoding="utf-8")
        json.dump(partidas, leaderboard, ensure_ascii=False, indent=4)
        leaderboard.close()
    except FileNotFoundError:
        leaderboard = open("Archivos/leaderboard", "w", encoding="utf-8")
        partidas = {}
        partidas[jugador['nombre']] = jugador
        json.dump(partidas, leaderboard, ensure_ascii=False, indent=4)
        leaderboard.close()
