from pattern.es import parse, split
from pattern.es import lexicon, spelling
from random import randrange

''' Funciones para chequear palabras dependiendo del nivel'''

def palabra_es_valida(palabra,*args):
    ''' Se ingresa la palabra y la cantidad de categorias para chequear
    nivel fácil = ingresar 1,2,3
    nivel medio = ingresar 1,2  //  1,3  //  2,3
    nivel díficil = ingresar 1 // 2 // 3'''
    es = False
    while(es == False):
        if(1 in args):
            es = es or es_sustantivo(palabra)
        if(2 in args):
            es = es or es_adjetivo(palabra)
        if(3 in args):
            es = es or es_verbo(palabra)
    return es

def es_sustantivo(palabra):
    p = parse(palabra).split()
    print(1)
    if(p[0][0][1] == 'NN'):
        return True
    else:
        return False

def es_adjetivo(palabra):
    p = parse(palabra).split()
    print(2)
    if(p[0][0][1] == 'JJ'):
        return True
    else:
        return False

def es_verbo(palabra):
    p = parse(palabra).split()
    print(3)
    if (p[0][0][1] == 'VB'):
        return True
    else:
        return False
