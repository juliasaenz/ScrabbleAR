import json

"""Diccionario de elementos que configuran un nivel"""
# Tablero
tablero: {
}

# Tiempo de la partida
tiempo = {
    "fácil": 300,
    "medio": 120,
    "difícil": 60
}

# Cantidad de letras
letras = {
    "fácil": dict(fácil={"a": 12, "e": 12, "i": 6, "o": 9, "u": 5,
                         "b": 2, "n": 5, "d": 5, "f": 1, "l": 4, "m": 2, "p": 2,
                         "g": 2, "h": 2, "v": 1, "c": 4, "r": 5, "s": 6,
                         "j": 1, "k": 1, "ñ": 1, "q": 1, "t": 4, "w": 1, "x": 1, "y": 1, "z": 1
                         }),
    "medio": dict(medio={"a": 11, "e": 11, "i": 6, "o": 8, "u": 6,
                         "b": 3, "n": 5, "d": 4, "f": 1, "l": 4, "m": 3, "p": 2,
                         "g": 2, "h": 2, "v": 1, "c": 4, "r": 5, "s": 7,
                         "j": 1, "k": 1, "ñ": 1, "q": 1, "t": 4, "w": 1, "x": 1, "y": 1, "z": 1
                         }),
    "difícil": dict(difícil={"a": 11, "e": 11, "i": 6, "o": 8, "u": 6,
                             "b": 3, "n": 5, "d": 4, "f": 1, "l": 4, "m": 3, "p": 2,
                             "g": 2, "h": 2, "v": 1, "c": 4, "r": 5, "s": 7,
                             "j": 1, "k": 1, "ñ": 1, "q": 1, "t": 4, "w": 1, "x": 1, "y": 1, "z": 1
                             })
}

# Puntos por letra
puntos = {
    "fácil": dict(fácil={"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "s": 1, "n": 1, "l": 1, "r": 1, "t": 1,
                         "c": 3, "d": 2, "g": 2,
                         "m": 3, "b": 3, "p": 3,
                         "f": 4, "h": 4, "v": 4, "y": 4,
                         "j": 6,
                         "k": 8, "ñ": 8, "z": 8,
                         "q": 10, "w": 10, "x": 10
                         }),
    "medio": dict(medio={"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "s": 1, "n": 1, "l": 1, "r": 1, "t": 1,
                         "c": 1, "d": 1, "g": 1,
                         "m": 2, "b": 2, "p": 2,
                         "f": 3, "h": 3, "v": 3, "y": 3,
                         "j": 5,
                         "k": 6, "ñ": 6, "z": 6,
                         "q": 8, "w": 8, "x": 8
                         }),
    "difícil": dict(difícil={"a": 0, "e": 0, "i": 0, "o": 0, "u": 0, "s": 0, "n": 0, "l": 0, "r": 0, "t": 0,
                             "c": 1, "d": 1, "g": 1,
                             "m": 2, "b": 2, "p": 2,
                             "f": 3, "h": 3, "v": 3, "y": 3,
                             "j": 5,
                             "k": 6, "ñ": 6, "z": 6,
                             "q": 8, "w": 8, "x": 8
                             })
}

# Dificultad de la computadora
compu = {
    "fácil": "facil",
    "medio": "medio",
    "difícil": "dificil"
}

# TABLERO ------- cambiar
tipos = {
    "fácil": ["normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal",
              "triple_palabra", "doble_palabra", "triple_letra", "doble_letra", "menos_uno", "menos_dos", "menos_tres"],
    "medio": ["normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal",
              "triple_palabra", "doble_palabra", "triple_letra", "doble_letra", "menos_uno", "menos_dos", "menos_tres"],
    "difícil": ["normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal",
                "triple_palabra", "doble_palabra", "triple_letra", "doble_letra", "menos_uno", "menos_dos",
                "menos_tres"]
}

# Categorias de palabras
categorias = {
    "fácil": [1, 2, 3],
    "medio": [2, 3],
    "difícil": [2, 3]
}

"""Diccionario de elementos que configuran un nivel"""
nivel = {
    # "tablero": tablero,
    "tiempo": tiempo,
    "letras": letras,
    "puntos": puntos,
    "compu": compu,
    "tipos": tipos,
    "palabras": categorias
}

# Cargar datos en un JSON
n = open("../Archivos/nivel", "w", encoding='utf-8')
json.dump(nivel, n, ensure_ascii=False, indent=4)
n.close()



