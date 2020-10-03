import json
from operator import getitem


def entra_en_top(puntaje):
    """ Calcula si el puntaje de la partida es mayor al último de los mejores 10 puntajes """
    try:
        leaderboard = open("Archivos/leaderboard", "r", encoding="utf-8")
        partidas = json.load(leaderboard)
        if len(partidas) < 10:
            return True
        else:
            for partida in partidas.keys():
                if partidas[partida]["puntaje"] < puntaje:
                    return True
            else:
                return False
        leaderboard.close()
    except FileNotFoundError:
        return True


def guardar_partida(jugador):
    """ Guarda el nombre y puntaje del usuario junto con la fecha y el nivel en el Top10 """
    try:
        leaderboard = open("Archivos/leaderboard", "r", encoding="utf-8")
        partidas = json.load(leaderboard)
        leaderboard.close()
        clave = jugador['nombre']
        i = 0

        while clave in partidas.keys():
            clave = jugador['nombre'] + str(i)
            i = i + 1

        partidas[clave] = jugador

        partidas = dict(sorted(partidas.items(), reverse=True,
                               key=lambda x: getitem(x[1], 'puntaje')))

        if len(partidas) > 10:
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
