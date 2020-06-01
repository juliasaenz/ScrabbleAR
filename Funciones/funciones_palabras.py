from pattern.es import parse, split
from pattern.es import lexicon, spelling
from random import randrange
import unicodedata

''' Funciones para chequear palabras dependiendo del nivel'''

def palabras_sin_tilde():
    ''' Esto crea un diccionario que tiene de clave
    las palabras sin tilde y de valor la palabra con
    tilde(en caso de tenerla) '''
    palabras = {}
    for palabra in lexicon:
        if(len(palabra) <= 7):
            pal = palabra
            trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
            pal = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', pal).translate(trans_tab))
            palabras[pal] = palabra
    return palabras

def existe_palabra(palabra,diccionario):
    '''Devuelve True si la palabra sin tilde existe entre las claves del diccionario'''
    if palabra in diccionario.keys():
        return True
    else:
        return False

def palabra_es_valida(palabra,diccionario,tipos):
    ''' Se ingresa la palabra y la cantidad de categorias para chequear
    nivel fácil = ingresar 1,2,3
    nivel medio = ingresar 1,2  //  1,3  //  2,3
    nivel díficil = ingresar 1 // 2 // 3'''
    es = False
    lista_verbos = ['VB', 'VBP', 'VBZ', 'VBG', 'VBD', 'VBN','MD']
    if(existe_palabra(palabra,diccionario)):
        p = parse(diccionario[palabra]).split()
        if(1 in tipos):
            es = es or (p[0][0][1] == 'NN')
        if(2 in tipos):
            es = es or (p[0][0][1] == 'JJ')
        if(3 in tipos):
            es = es or (p[0][0][1] in lista_verbos)
    return es

