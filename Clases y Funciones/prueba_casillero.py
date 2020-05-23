import json
from Casillero import Casillero
from Tablero import Tablero

archivo = open("diccionario","r")
diccionario = json.load(archivo)
print(diccionario)

tabla = Tablero()
tabla.dibujar_tablero()
tabla.imprimir_tablero()
