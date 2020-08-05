""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

import estilo
import random
from random import randrange
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
    if event == "JUGAR" or event == "go":
        window.close()
        # ----- INICIO
        inicio = inicio()
        turno = Turno()
        window = sg.Window("ScrabbleAR").Layout(inicio)
        event, values = window.read()
    if event == "Nueva Partida":
        window.close()
        # CONFIGURAR NIVEL ----
        nivel = open("Archivos/nivel", "r", encoding="utf-8")
        niveles = json.load(nivel)
        # Si no elige ningun nivel o elige customizar, inicializa la confuración en nivel fácil
        if len(values[1]) == 0 or values[1][0] == 'customizar':
            config = {
                "puntos": niveles["puntos"]["fácil"]["fácil"],
                "tiempo": niveles["tiempo"]["fácil"],
                "cantidad": niveles["letras"]["fácil"]["fácil"],
                "palabras": niveles["palabras"]["fácil"],
                "tipos": niveles["tipos"]["fácil"],
                "compu": niveles["compu"]["fácil"]
            }
            # --- Arreglo de Strings que guarda el nivel general y de cada elelemtento
            for i in range(7):
                act_config.append("fácil")
            # --- Si el se eligio customizar, abre la ventana de customización de nivel
            # Todoo aquel casillero que no rellene, quedará como nivel fácil
            if len(values[1]) != 0 and values[1][0] == 'customizar':
                t = configurar_dificultad(config, niveles, Jugador.bolsa, 0, act_config)
                if t is not None:
                    tiempo = t
        elif values[1][0] == 'aleatorio':
            # --- Arma una configuración aleatoria
            act_config.append("aleatorio")
            opciones = ["fácil", "medio", "difícil"]
            config = {}
            # compu
            aux = opciones[randrange(3)]
            config["compu"] = niveles["compu"][aux]
            act_config.append(aux)
            # cantidad de fichas
            aux = opciones[randrange(3)]
            config["cantidad"] = niveles["letras"][aux][aux]
            act_config.append(aux)
            # puntos de fichas
            aux = opciones[randrange(3)]
            config["puntos"] = niveles["puntos"][aux][aux]
            act_config.append(aux)
            # tablero
            aux = opciones[randrange(3)]
            config["tipos"] = niveles["tipos"][aux]
            act_config.append(aux)
            # tiempo
            aux = opciones[randrange(3)]
            config["tiempo"] = niveles["tiempo"][aux]
            act_config.append(aux)
            # palabras
            aux = opciones[randrange(3)]
            config["palabras"] = niveles["palabras"][aux]
            act_config.append(aux)
        else:
            # --- Si elige un nivel, inicializa ese
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
        # JUGADORES----
        jugador = Jugador(values[0])
        compu = Computadora()
        # TABLERO----
        tabla = Tablero(config["tipos"])
    elif event == "Continuar":
        # --- Si decide continuar una partida y esta existe
        try:
            window.close()
            # NIVEL----
            nivel = open("Archivos/nivel", "r", encoding="utf-8")
            niveles = json.load(nivel)
            # ARCHIVO----
            continuar = True
            archivo = open("Archivos/ultima_partida.txt", "r", encoding="UTF-8")
            partida = json.load(archivo)
            config = partida["nivel"]
            # DICCIONARIO----
            diccionario = palabras_sin_tilde()
            # BOLSA----
            Jugador.bolsa = partida["bolsa"]
            # JUGADORES----
            jugador = Jugador(partida["jugador"]["nombre"])
            compu = Computadora()
            # TABLERO----
            tabla = Tablero(config["tipos"])
            # Restaurar datos
            jugador.continuar_turno(partida["jugador"])
            compu.continuar_turno(partida["compu"])
            tabla.continuar_partida(partida["tablero"])
            turno.set_turno_usuario(partida["turno"])
            turno.set_lista_palabras(partida["palabras_jugadas"])
            act_config = partida["act_config"]
        except FileNotFoundError:
            # Si no hay un archivo de partida guardado, salta el PopUp y se cierra el programa
            sg.Popup("¡ERROR! No hay ninguna partida guardada", **estilo.tt)

    # --- Columna de botones
    try:
        col = [[sg.Text("NIVEL: {}".format(act_config[0].upper()), key="nivel", **estilo.tt)],
               [sg.Button("Reglas", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
               [sg.Button("Configuración actual", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
               [sg.Button("Palabras Jugadas", key="palabras", button_color=("#FAFAFA", "#151514"),
                          **estilo.tt)],
               [sg.Frame(layout=[[sg.Text('{}'.format(config["tiempo"]), key="tiempo", **estilo.tp)]],
                         title="Tiempo", key="tiempo_f", **estilo.tt)],
               [sg.Button('', image_data=estilo.red_x_base64, key='g',
                          button_color=(sg.theme_background_color(),
                                        sg.theme_background_color()), border_width=0)],
               [sg.Button("Pausar Partida", key="pausa", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
               [sg.Ok("Terminar Partida", button_color=("#FAFAFA", "#151514"), **estilo.tt)]
               ]
    except IndexError:
        sg.Popup("Se cerró la aplicación antes de tiempo")

    # --- Layut del juego
    ventana_juego = [
        [sg.Frame(layout=compu.dibujar(), key=compu.get_nombre(),
                  title="Atril de " + compu.get_nombre(), **estilo.tt), sg.Text("Puntaje: ", **estilo.tt),
         sg.Text(" {} ".format(jugador.get_puntaje()), key="p_compu", **estilo.tt),
         sg.Button("Top Ten Puntajes", key="top", button_color=("#FAFAFA", "#151514"), **estilo.tt),
         sg.Button("Configuración", key="configuracion", button_color=("#FAFAFA", "#151514"),
                   **estilo.tt)],
        [sg.Column(col), sg.Frame(layout=tabla.dibujar(), title="Tablero", **estilo.tt)],
        [],
        [sg.Frame(layout=jugador.dibujar(), key=jugador.get_nombre(),
                  title="Atril de " + jugador.get_nombre(), **estilo.tt),
         sg.Text("Puntaje: ", **estilo.tt),
         sg.Text(" {} ".format(jugador.get_puntaje()), key="p_jugador", **estilo.tt),
         sg.Button("Shuffle", button_color=("#FAFAFA", "#151514"), **estilo.tt),
         sg.Button("Limpiar", button_color=("#FAFAFA", "#151514"), **estilo.tt),
         sg.Ok("Terminar Turno", button_color=("#FAFAFA", "#151514"), **estilo.tt)
         ]
    ]

    # --- Ventana
    window = sg.Window("ScrabbleAR", ventana_juego, grab_anywhere=True)
    window.Read(timeout=0)
    if continuar:
        # --- Si se continua partida, pinta los casilleros bloqueados del color correspondiente
        # y marca el primer turno como jugado
        turno.jugue_primer_turno()
        jugador.add_casilleros_usados(partida["jugador"]["casilleros"])
        compu.add_casilleros_usados(partida["compu"]["casilleros"])
        for pos in partida["jugador"]["casilleros"]:
            window.FindElement((int(pos[0]), int(pos[1]))).Update(button_color=("white", "#6A0642"))
        for pos in partida["compu"]["casilleros"]:
            window.FindElement((int(pos[0]), int(pos[1]))).Update(button_color=("white", "#06586A"))

except NameError:
    # Si se cierra en la ventana de inicio o de tutorial
    tiempo = -1

try:
    tiempo = config["tiempo"] * 100
except NameError:
    # Si se cierra en la ventana de inicio o de tutorial
    tiempo = -1
