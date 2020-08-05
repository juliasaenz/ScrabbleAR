""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

import json

"""Diccionario de elementos que configuran un nivel"""
# Tablero
tablero: {
}

# Tiempo de la partida
tiempo = {
    "fácil": 180,
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
    "medio": dict(medio={"a": 11, "e": 11, "i": 6, "o": 8, "u": 5,
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
    "difícil": dict(difícil={"a": 0, "e": 0, "i": 0, "o": 0, "u": 0, "s": 0,
                             "n": 1, "l": 1, "r": 1, "t": 1,
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
tab = []
for x in range(15):
    tab.append([])
    for y in range(15):
        if x == y or x + y == 14:
            if x == 7:
                tab[x].append("normal")
            elif x == 4 or x == 9:
                tab[x].append("triple_letra")
            elif x == 6 or x == 8:
                tab[x].append("doble_letra")
            elif x == 0 or x == 14:
                tab[x].append("triple_palabra")
            else:
                tab[x].append("doble_palabra")
        elif x == 7 and y != 7:
            if y % 2 == 0:
                tab[x].append("doble_letra")
            else:
                tab[x].append("normal")
        elif y == 7 and x != 7:
            if x % 2 == 0:
                tab[x].append("doble_letra")
            else:
                tab[x].append("normal")
        elif (x + y == 21 or x + y == 7) and (x == 0 or x == 14 or y == 0 or y == 14):
            tab[x].append("triple_palabra")
        elif ((x == 0 or x == 14) and (y == 4 or y == 10)) or ((y == 0 or y == 14) and (x == 4 or x == 10)):
            tab[x].append("triple_letra")
        elif (x == 9 or x == 12 or x == 5 or x == 2) and (y == 9 or y == 12 or y == 5 or y == 2):
            tab[x].append("menos_dos")
        elif (x == 0 or y == 0 or x == 14 or y == 14) and ((y + x) % 2 == 0):
            tab[x].append("menos_uno")
        else:
            tab[x].append("normal")

tab2 = []
for x in range(15):
    tab2.append([])
    for y in range(15):
        if x == y or x + y == 14:
            if x == 7:
                tab2[x].append("normal")
            elif x == 4 or x == 9:
                tab2[x].append("doble_palabra")
            elif x == 6 or x == 8:
                tab2[x].append("doble_letra")
            elif x == 0 or x == 14:
                tab2[x].append("triple_palabra")
            else:
                tab2[x].append("triple_letra")
        elif x == 7 and y != 7:
            if y % 2 == 0:
                tab2[x].append("menos_uno")
            else:
                tab2[x].append("normal")
        elif y == 7 and x != 7:
            if x % 2 == 0:
                tab2[x].append("menos_uno")
            else:
                tab2[x].append("normal")
        elif (x + y == 21 or x + y == 7) and (x == 0 or x == 14 or y == 0 or y == 14):
            tab2[x].append("triple_palabra")
        elif ((x == 0 or x == 14) and (y == 4 or y == 10)) or ((y == 0 or y == 14) and (x == 4 or x == 10)):
            tab2[x].append("menos_tres")
        elif (x == 9 or x == 12 or x == 5 or x == 2) and (y == 9 or y == 12 or y == 5 or y == 2):
            tab2[x].append("menos_dos")
        elif (x == 0 or y == 0 or x == 14 or y == 14) and ((y + x) % 2 == 0):
            tab2[x].append("doble_letra")
        else:
            tab2[x].append("normal")

tab3 = []
for x in range(15):
    tab3.append([])
    for y in range(15):
        if x == y or x + y == 14:
            if x == 7:
                tab3[x].append("normal")
            elif x == 4 or x == 10:
                tab3[x].append("doble_palabra")
            elif x == 6 or x == 8:
                tab3[x].append("triple_letra")
            elif x == 0 or x == 14:
                tab3[x].append("triple_palabra")
            else:
                tab3[x].append("menos_dos")
        elif x == 7 and y != 7:
            if y % 2 == 0:
                tab3[x].append("doble_letra")
            else:
                tab3[x].append("menos_uno")
        elif y == 7 and x != 7:
            if x % 2 == 0:
                tab3[x].append("doble_letra")
            else:
                tab3[x].append("menos_uno")
        elif ((x == 0 or x == 14) and (y == 4 or y == 10)) or ((y == 0 or y == 14) and (x == 4 or x == 10)):
            tab3[x].append("doble_palabra")
        elif (x == 9 or x == 12 or x == 5 or x == 2) and (y == 9 or y == 12 or y == 5 or y == 2):
            tab3[x].append("triple_letra")
        elif (x == 0 or y == 0 or x == 14 or y == 14) and ((y + x) % 2 == 0):
            tab3[x].append("menos_tres")
        else:
            tab3[x].append("normal")

# TABLERO ------- cambiar
tipos = {
    "fácil": tab,
    "medio": tab2,
    "difícil": tab3
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
