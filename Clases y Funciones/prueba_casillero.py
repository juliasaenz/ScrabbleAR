import json
from Casillero import Casillero
from Tablero import Tablero

archivo = open("diccionario","r")
diccionario = json.load(archivo)
print(diccionario["a"])

tabla = Tablero()
tabla.imprimir_tablero()
