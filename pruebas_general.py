import json
import sys
from Clases.Tablero import Tablero
from Clases.Jugador import Jugador
from Clases.Interfaz import Interfaz
from Funciones.funciones_palabras import palabra_es_valida, palabras_sin_tilde

# diccionario de palabras váidas
diccionario = palabras_sin_tilde()

#nivel
nivel = open("Archivos/nivel1","r")
config = json.load(nivel)

#lista
bolsa = []
for letra in config["cantidad"].keys():
    for veces in range(config["cantidad"][letra]):
        bolsa.append(letra)
print(len(bolsa))

#juego
tabla = Tablero()
jugador = Jugador("julia",bolsa)

jugador.imprimir_atril()
#ficha = input("que ficha saco? ")
#jugador.sacar_ficha(ficha)
#jugador.imprimir_atril()
#jugador.reponer_atril(bolsa)
#jugador.imprimir_atril()

#print("bolsa: ",jugador.bolsa)
#tabla.imprimir_tablero()

interfaz = Interfaz(tabla,jugador)
interfaz.mostrar_interfaz()
