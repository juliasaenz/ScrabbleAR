import json
import sys
import time
from Clases.Tablero import Tablero
from Clases.Jugador import Jugador
from Clases.Computadora import Computadora
from Clases.Turno import Turno
from Funciones.funciones_palabras import palabra_es_valida, palabras_sin_tilde
from Funciones.Ventanas_extra import tutorial, inicio
import PySimpleGUI as sg
from random import randrange

# ------ TUTORIAL
tutorial = tutorial()
window = sg.Window("ScrabbleAR").Layout(tutorial)
event, values = window.read()

if event == None:
    window.close()
if event == "Ok":
    window.close()
    inicio = inicio()

    window = sg.Window("ScrabbleAR").Layout(inicio)
    event, values = window.read()
    if (event == "Nueva Partida"):
        window.close()
        print("values: ",values)
        #NIVEL----
        if(len(values[1]) == 0 or values[1][0] == "Nivel 1"):
            nivel = open("Archivos/nivel1", "r",encoding="utf-8")
        elif(values[1][0] == "Nivel 2"):
            nivel = open("Archivos/nivel2", "r",encoding="utf-8")
        elif (values[1][0] == "Nivel 3"):
            nivel = open("Archivos/nivel3", "r",encoding="utf-8")
        config = json.load(nivel)
        #DICCIONARIO----
        diccionario = palabras_sin_tilde()
        #BOLSA-----
        for letra in config["cantidad"].keys():
            for veces in range(config["cantidad"][letra]):
                Jugador.bolsa.append(letra)
        #JUGADORES ---
        jugador = Jugador(values[0])
        compu = Computadora()
        #TABLERO ---
        tabla = Tablero(config["tipos"])
    elif (event == "Continuar"):
        archivo = open("ultima_partida.txt","r",encoding="UTF-8")
        partida = json.load(archivo)
        config = partida["nivel"]
        # DICCIONARIO----
        diccionario = palabras_sin_tilde()
        #BOLSA
        Jugador.bolsa = partida["bolsa"]
        # JUGADORES ---
        jugador = Jugador(partida["jugador"]["nombre"])
        compu = Computadora()
        # TABLERO ---
        tabla = Tablero(config["tipos"])
        #Restaurar datos
        jugador.continuar_turno(partida["jugador"])
        compu.continuar_turno(partida["compu"])
        tabla.continuar_partida(partida["tablero"])



    ventana_juego = [[sg.Button("Reglas", button_color=("black","#FAFAFA")),sg.Button("Pausar Partida",key="pausa", button_color=("black","#FAFAFA"))],
                         [sg.Frame(layout=compu.dibujar(),key = compu.get_nombre(),
                                   title = "Atril de " + compu.get_nombre()),sg.Text("Puntaje: "),sg.Text("  0  ",key = "p_compu")],
                        [sg.Frame(layout=tabla.dibujar(), title="Tablero"),sg.Text('Tiempo: {}'.format(config["tiempo"]), key = "tiempo")],
                         [],
                         [sg.Frame(layout=jugador.dibujar(), key=jugador.get_nombre(),
                                   title="Atril de " + jugador.get_nombre()),
                          sg.Button("Shuffle"),sg.Button("Limpiar"), sg.Ok("Terminar Turno"),sg.Text("Puntaje: "),sg.Text("  0  ",key = "p_jugador")]
                         ]
    window = sg.Window("ScrabbleAR").Layout(ventana_juego)

    # bloquear las usadas
    window.Read(timeout=0)
    for x in range(15):
        for y in range(15):
            if (tabla.esta_bloqueado((x, y))):
                try:
                    window.FindElement((x, y)).Update(button_color=("white", "black"))
                except(TypeError):
                    print(x, y)

