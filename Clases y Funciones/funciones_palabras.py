from pattern.es import parse, split
from pattern.es import lexicon, spelling
from random import randrange
import unicodedata

''' Funciones para chequear palabras dependiendo del nivel'''

def palabras_sin_tilde():
    '''
    Esto crea un diccionario que tiene de clave las palabras sin tilde y de valor la palabra con tilde(en caso de tenerla)
    '''
    palabras = {}
    for palabra in lexicon:
            pal = palabra
            trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
            pal = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', pal).translate(trans_tab))
            palabras[pal] = palabra
    return palabras

#Funciones para definir cada tipo de palabra
def es_sustantivo(palabra):
    ''' True si la palabra es un sustantivo'''
    p = parse(palabra).split()
    if(p[0][0][1] == 'NN'):
        return True
    else:
        return False

def es_adjetivo(palabra):
    ''' True si la palabra es adjetivo'''
    p = parse(palabra).split()
    if(p[0][0][1] == 'JJ'):
        return True
    else:
        return False

def es_verbo(palabra):
    ''' True si la palabra es verbo'''
    p = parse(palabra).split()
    lista_verbos = ['VB','VBP','VBZ','VBG','VBD','VBN']
    if (p[0][0][1] in lista_verbos):
        return True
    else:
        return False

#arreglarlo
def palabra_es_valida(palabra,diccionario,*args):
    ''' Se ingresa la palabra y la cantidad de categorias para chequear
    nivel fácil = ingresar 1,2,3
    nivel medio = ingresar 1,2  //  1,3  //  2,3
    nivel díficil = ingresar 1 // 2 // 3'''
    es = False
    if(existe_aca(palabra,diccionario)):
        while(es == False):
            if(1 in args):
                es = es or es_sustantivo(diccionario[palabra])
            if(2 in args):
                es = es or es_adjetivo(diccionario[palabra])
            if(3 in args):
                es = es or es_verbo(diccionario[palabra])
    return es

def existe_aca(palabra,diccionario):
    if palabra in diccionario.keys():
        return diccionario[palabra]
    else:
        return False


diccionario = palabras_sin_tilde()
print(palabra_es_valida("tenia",diccionario,1,2,3))