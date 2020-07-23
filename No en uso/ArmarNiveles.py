import json

# -*- coding: utf-8 -*-

''' Creamos el nivel y lo guardamos en un txt'''
n1 = open("../Archivos/nivel1", "w", encoding='utf-8')
datos_n1 = {}

# nivel 1
puntos = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "s": 1, "n": 1, "l": 1, "r": 1, "t": 1,
          "c": 3, "d": 2, "g": 2,
          "m": 3, "b": 3, "p": 3,
          "f": 4, "h": 4, "v": 4, "y": 4,
          "j": 8, "k": 8, "ñ": 8, "z": 8,
          "q": 10, "w": 10, "x": 10}
tiempo_turno = 100
cantidad = {"a": 12, "e": 12, "i": 6, "o": 9, "u": 5,
            "b": 2, "n": 5, "d": 5, "f": 1, "l": 4, "m": 2, "p": 2,
            "g": 2, "h": 2, "v": 1, "c": 4, "r": 5, "s": 6,
            "j": 1, "k": 1, "ñ": 1, "q": 1, "t": 4, "w": 1, "x": 1, "y": 1, "z": 1
            }
categorias_palabras = [1, 2, 3]
tipos = ["normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal",
         "triple_palabra", "doble_palabra", "triple_letra", "doble_letra", "menos_uno", "menos_dos", "menos_tres"]
datos_n1 = {"puntos": puntos,
            "tiempo": tiempo_turno,
            "cantidad": cantidad,
            "palabras": categorias_palabras,
            "tipos": tipos}

json.dump(datos_n1, n1, ensure_ascii=False, indent=4)
n1.close()

''' Creamos el nivel y lo guardamos en un txt'''
n2 = open("../Archivos/nivel2", "w", encoding='utf-8')
datos_n2 = {}

# nivel 2
puntos = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "s": 1, "n": 1, "l": 1, "r": 1, "t": 1,
          "c": 3, "d": 2, "g": 2,
          "m": 3, "b": 3, "p": 3,
          "f": 4, "h": 4, "v": 4, "y": 4,
          "j": 8,
          "k": 8, "ñ": 8, "z": 8,
          "q": 10, "w": 10, "x": 10}
tiempo_turno = 60
cantidad = {"a": 12, "e": 12, "i": 6, "o": 9, "u": 5,
            "b": 2, "n": 5, "d": 5, "f": 1, "l": 4, "m": 2, "p": 2,
            "g": 2, "h": 2, "v": 1, "c": 4, "r": 5, "s": 6,
            "j": 1, "k": 1, "ñ": 1, "q": 1, "t": 4, "w": 1, "x": 1, "y": 1, "z": 1
            }
categorias_palabras = [1, 2, 3]
tipos = ["normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal",
         "triple_palabra", "doble_palabra", "triple_letra", "doble_letra", "menos_uno", "menos_dos", "menos_tres"]
datos_n2 = {"puntos": puntos,
            "tiempo": tiempo_turno,
            "cantidad": cantidad,
            "palabras": categorias_palabras,
            "tipos": tipos}

json.dump(datos_n2, n2, ensure_ascii=False, indent=4)
n2.close()

# nivel 3
n3 = open("../Archivos/nivel3", "w", encoding='utf-8')
datos_n3 = {}

puntos = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "s": 1, "n": 1, "l": 1, "r": 1, "t": 1,
          "c": 3, "d": 2, "g": 2,
          "m": 3, "b": 3, "p": 3,
          "f": 4, "h": 4, "v": 4, "y": 4,
          "j": 8,
          "k": 8, "ñ": 8, "z": 8,
          "q": 10, "w": 10, "x": 10}
tiempo_turno = 30
cantidad = {"a": 12, "e": 12, "i": 6, "o": 9, "u": 5,
            "b": 2, "n": 5, "d": 5, "f": 1, "l": 4, "m": 2, "p": 2,
            "g": 2, "h": 2, "v": 1, "c": 4, "r": 5, "s": 6,
            "j": 1, "k": 1, "ñ": 1, "q": 1, "t": 4, "w": 1, "x": 1, "y": 1, "z": 1
            }
categorias_palabras = [1, 2, 3]
tipos = ["normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal", "normal",
         "triple_palabra", "doble_palabra", "triple_letra", "doble_letra", "menos_uno", "menos_dos", "menos_tres"]
datos_n3 = {"puntos": puntos,
            "tiempo": tiempo_turno,
            "cantidad": cantidad,
            "palabras": categorias_palabras,
            "tipos": tipos}

json.dump(datos_n3, n3, ensure_ascii=False, indent=4)
n3.close()
