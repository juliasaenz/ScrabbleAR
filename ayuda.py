import itertools as it
from Funciones.funciones_palabras import palabra_es_valida
from Funciones.funciones_palabras import palabras_sin_tilde

# DICCIONARIO----
diccionario = palabras_sin_tilde()

letras = ["k", "b", "i", "o", "e", "a", "w"]
palabras = set()
pal = ""
for i in range(2, len(letras) + 1):
    palabras.update((map("".join, it.permutations(letras, i))))
for i in palabras:
    # recibe diccionario y tipos de palabras que acepta
    if palabra_es_valida(i, diccionario, [2,3]):
        if len(i) > len(pal):
            pal = i

print(pal)