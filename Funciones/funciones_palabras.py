""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from pattern.es import parse, split
from pattern.es import lexicon, spelling
from random import randrange
import unicodedata

''' Funciones para la validación de palabras'''


def tiene_estas(palabra):
    """ Devuelve si la palabra pasada por parámetro incluye un número o signo de puntuación"""
    sacar = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "#", "!", "*", "-", "/", "<", ">", "."]
    hay = False
    for i in sacar:
        if i in palabra:
            hay = True
    return hay


def palabras_sin_tilde():
    """ Crea un diccionario que tiene de clave
    las palabras sin tilde y de valor la palabra con
    tilde(en caso de tenerla). Solo agrega palabras entre
    2 y 7 letras que no tengan números o signos de puntuación"""
    palabras = {}
    for palabra in lexicon.keys():
        if 2 <= len(palabra) <= 7 and not tiene_estas(palabra):
            pal = palabra.lower()
            trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
            pal = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', pal).translate(trans_tab))
            palabras[pal] = palabra.lower()
    return palabras


def existe_palabra(palabra, diccionario):
    """Devuelve True si la palabra sin tilde existe entre las claves del diccionario"""
    if palabra in diccionario.keys():
        return True
    else:
        return False


def palabra_es_valida(palabra, diccionario, lista):
    """ Se ingresa la palabra y la cantidad de categorias para chequear
    \n nivel fácil = ingresar 1, 2
    \n nivel medio = ingresar 2
    \n nivel díficil = ingresar 2  """
    es = False
    lista_sus = ["NC", "NN", "NCS", "NCP", "NNS", "NP", "NNP", "W"]
    lista_adj = ["AO", "JJ", "AQ", "DI", "DT"]
    lista_verbos = ['VB', 'VBP', 'VBZ', 'VBG', 'VBD', 'VBN', 'MD']
    if existe_palabra(palabra, diccionario):
        p = parse(diccionario[palabra]).split()
        if 1 in lista:
            es = es or (p[0][0][1] in lista_sus)
        if 2 in lista:
            es = es or (p[0][0][1] in lista_adj or p[0][0][1] in lista_verbos)
    return es
