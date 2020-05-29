import json
from Casillero import Casillero
from Tablero import Tablero
from Interfaz import Interfaz

archivo = open("diccionario","r")
diccionario = json.load(archivo)
print(diccionario)

tabla = Tablero()
#tabla.imprimir_tablero()
interfaz = Interfaz(tabla)
interfaz.mostrar_interfaz()
tabla.imprimir_tablero()