""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

import estilo
import random
from Clases.Tablero import Tablero
from Clases.Jugador import Jugador
from Clases.Computadora import Computadora
from Clases.Turno import Turno
from Funciones.funciones_palabras import palabras_sin_tilde
from Funciones.Ventanas_secundarias import tutorial, inicio, configurar_dificultad, ventana_shuffle
from Funciones.funciones_partida import *
import PySimpleGUI as sg

# ------ TUTORIAL
tutorial = tutorial()
window = sg.Window("ScrabbleAR").Layout(tutorial)
event, values = window.read()

# ------
act_config = []
continuar = False

try:
    if event is None:
        window.close()
    if event == "Ok":
        window.close()
        inicio = inicio()
        turno = Turno()
        window = sg.Window("ScrabbleAR").Layout(inicio)
        event, values = window.read()
    if event == "Nueva Partida":
        window.close()
        print("values: ", values)
        # NIVEL----
        nivel = open("Archivos/nivel", "r", encoding="utf-8")
        niveles = json.load(nivel)
        if len(values[1]) == 0 or values[1][0] == 'customizar':
            config = {
                "puntos": niveles["puntos"]["fácil"]["fácil"],
                "tiempo": niveles["tiempo"]["fácil"],
                "cantidad": niveles["letras"]["fácil"]["fácil"],
                "palabras": niveles["palabras"]["fácil"],
                "tipos": niveles["tipos"]["fácil"],
                "compu": niveles["compu"]["fácil"]
            }

            for i in range(7):
                act_config.append("fácil")

            if len(values[1]) != 0 and values[1][0] == 'customizar':
                t = configurar_dificultad(config, niveles, Jugador.bolsa, 0)
                if t is not None:
                    tiempo = t
        else:
            config = {
                "puntos": niveles["puntos"][values[1][0]][values[1][0]],
                "tiempo": niveles["tiempo"][values[1][0]],
                "cantidad": niveles["letras"][values[1][0]][values[1][0]],
                "palabras": niveles["palabras"][values[1][0]],
                "tipos": niveles["tipos"][values[1][0]],
                "compu": niveles["compu"][values[1][0]]
            }

            for i in range(7):
                act_config.append(values[1][0])

        # DICCIONARIO----
        diccionario = palabras_sin_tilde()
        # BOLSA-----
        for letra in config["cantidad"].keys():
            for veces in range(config["cantidad"][letra]):
                Jugador.bolsa.append(letra)
        # JUGADORES ---
        jugador = Jugador(values[0])
        compu = Computadora()
        # TABLERO ---
        tabla = Tablero(config["tipos"])
    elif event == "Continuar":
        continuar = True
        archivo = open("ultima_partida.txt", "r", encoding="UTF-8")
        partida = json.load(archivo)
        config = partida["nivel"]
        # DICCIONARIO----
        diccionario = palabras_sin_tilde()
        # BOLSA
        Jugador.bolsa = partida["bolsa"]
        # JUGADORES ---
        jugador = Jugador(partida["jugador"]["nombre"])
        compu = Computadora()
        # TABLERO ---
        tabla = Tablero(config["tipos"])
        # Restaurar datos
        jugador.continuar_turno(partida["jugador"])
        compu.continuar_turno(partida["compu"])
        tabla.continuar_partida(partida["tablero"])
        turno.set_lista_palabras(partida["palabras_jugadas"])

    col = [[sg.Button("Reglas", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Button("Top Ten Puntajes", key="top", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Button("Configuración", key="configuracion", button_color=("#FAFAFA", "#151514"),
                      **estilo.tt)],
           [sg.Button("Configuración actual", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
           [sg.Button("Palabras Jugadas", key="palabras", button_color=("#FAFAFA", "#151514"),
                      **estilo.tt)],
           [sg.Text('\n')], [sg.Text('\n')],
           [sg.Frame(layout=[[sg.Text('{}'.format(config["tiempo"]), key="tiempo", **estilo.tp)]],
                     title="Tiempo", key="tiempo_f", **estilo.tt)],
           [sg.Text('\n')], [sg.Text('\n')], [sg.Text('\n')],
           [sg.Button("Shuffle", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Button("Limpiar", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Ok("Terminar Turno", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Button("Pausar Partida", key="pausa", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Ok("Terminar Partida", button_color=("#FAFAFA", "#151514"), **estilo.tt)]
           ]

    ventana_juego = [
        [sg.Frame(layout=compu.dibujar(), key=compu.get_nombre(),
                  title="Atril de " + compu.get_nombre(), **estilo.tt), sg.Text("Puntaje: ", **estilo.tt),
         sg.Text("  0  ", key="p_compu", **estilo.tt)],
        [sg.Column(col), sg.Frame(layout=tabla.dibujar(), title="Tablero", **estilo.tt)],
        [],
        [sg.Frame(layout=jugador.dibujar(), key=jugador.get_nombre(),
                  title="Atril de " + jugador.get_nombre(), **estilo.tt),
         sg.Text("Puntaje: ", **estilo.tt),
         sg.Text("  0  ", key="p_jugador", **estilo.tt)]
    ]

    window = sg.Window("ScrabbleAR", ventana_juego, grab_anywhere=True)

    # bloquear las usadas
    '''window.Read(timeout=0)
    for x in range(15):
        for y in range(15):
            if tabla.esta_bloqueado((x, y)):
                try:
                    window.FindElement((x, y)).Update(button_color=("white", "black"))
                except TypeError:
                    print(x, y)'''

    if continuar:
        window.Read(timeout=0)
        for pos in partida["jugador"]["casilleros"]:
            window.FindElement((int(pos[0]), int(pos[1]))).Update(button_color=("white", "#D92335"))
            print(int(pos[0]), pos[1])
        for pos in partida["compu"]["casilleros"]:
            window.FindElement((int(pos[0]), int(pos[1]))).Update(button_color=("white", "#4B3588"))
            print(int(pos[0]), pos[1])

except NameError:
    # Si se cierra en la ventana de inicio o de tutorial
    tiempo = -1

try:
    tiempo = config["tiempo"] * 100
except NameError:
    tiempo = -1

