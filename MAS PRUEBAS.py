import json
import sys
from Clases.Tablero import Tablero
from Clases.Jugador import Jugador
from Funciones.funciones_palabras import palabra_es_valida, palabras_sin_tilde
from Funciones.diagrama import tutorial
import PySimpleGUI as sg
estado = "inicio"

#INICIO

# armo el diccionario de palabras válidas
diccionario = palabras_sin_tilde()

# abro el json del nivel que quiera
nivel = open("Archivos/nivel1", "r")
config = json.load(nivel)

# armo la bolsa de letras (es una lista)
bolsa = []
for letra in config["cantidad"].keys():
    for veces in range(config["cantidad"][letra]):
        bolsa.append(letra)

#abro el tutorial
tutorial = tutorial()
window = sg.Window("ScrabbleAR").Layout(tutorial)
event, values = window.read()

jugador = Jugador("Julia",bolsa)

#paso a juego
if event == None:
    window.close()
if event == "Jugar":
    window.close()
    tabla = Tablero()

    # variables
    letra_act = ""
    boton = list(range(15 * 15))

    #JUGAR
    ventana_juego = [[sg.Frame(layout=tabla.dibujar(), title="Tablero")],
                     [],
                     [sg.Frame(layout=jugador.dibujar(), title="Atril de "+jugador.get_nombre())]
                     ]
    window = sg.Window("ScrabbleAR").Layout(ventana_juego)
    while True:
        event, values = window.read()
        if (event == None):
            break
        if (event in boton):
            window.FindElement(event).Update(letra_act)
            letra_act = ""
        else:
            letra_act = event