import json

# -*- coding: utf-8 -*-

''' Creamos el diccionario y lo guardamos en un txt'''
diccionario = open("diccionario", "w", encoding='utf-8')

#Diccionario
dicc = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "s": 1, "n": 1, "l": 1, "r": 1, "t": 1,
        "c": 2, "d": 2, "g": 2,
        "m": 3, "b": 3, "p": 3,
        "f": 4, "h": 4, "v": 4, "y": 4,
        "j": 6,
        "k": 8, "ñ": 8, "z": 8,
        "q": 10, "w": 10, "x": 10}

json.dump(dicc,diccionario)
diccionario.close()