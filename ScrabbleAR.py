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

try:
    if event is None:
        window.close()
    if event == "Ok":
        window.close()
        inicio = inicio()

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

    col = [[sg.Button("Reglas", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Button("Top Ten Puntajes", key="top", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
           [sg.Button("Pausar Partida", key="pausa", button_color=("#FAFAFA", "#151514"), **estilo.tt)],
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
    window.Read(timeout=0)
    for x in range(15):
        for y in range(15):
            if tabla.esta_bloqueado((x, y)):
                try:
                    window.FindElement((x, y)).Update(button_color=("white", "black"))
                except TypeError:
                    print(x, y)
except NameError:
    tiempo = -1

turno = Turno()
try:
    tiempo = config["tiempo"] * 100
except NameError:
    tiempo = -1


def timer():
    """ Actualiza el temporizador """
    global tiempo
    tiempo = tiempo - 1
    # print("tiempo: ", tiempo)
    # --------- Display timer in window --------
    window["tiempo"].update('{}'.format(int(tiempo / 100)))


# -------------------------------------------
#                  JUEGO
# -------------------------------------------

# Quien empieza
# turno.set_turno_usuario(bool(random.getrandbits(1)))
turno.set_turno_usuario(False)

# Tiempo es -1 cuando se cerro la ventana de Tutorial o Inicio
if tiempo != -1:
    while True:
        timer()
        event, values = window.read(timeout=10)
        # ----- SI ES EL TURNO DEL USUARIO Y NO TERMINO LA PARTIDA
        if jugador.get_cant_bolsa() != 0 and tiempo != 0:
            if turno.es_turno_usuario():
                if event != "__TIMEOUT__":
                    print("event: ", event)
                if event is None:
                    break
                # --- si toco un boton del tablero
                elif event in tabla.get_posiciones():
                    if turno.get_letra_actual() != "":
                        # si el casillero no esta bloqueado
                        if not tabla.esta_bloqueado(event):
                            # si el casillero esta vacio
                            if tabla.get_casillero(event) == "":
                                poner_ficha(event, turno, tabla, window)
                        # actualizo letra actual
                        turno.set_letra_actual("")
                        turno.set_pos_actual("")
                # --- si toco un boton del atril
                elif event in "0123456":
                    letra_actual(event, turno, jugador)
                elif event == "Limpiar":
                    limpiar(turno, tabla, window)
                elif event == "Shuffle":
                    window.Hide()
                    shuffle(turno, tabla, jugador, window, config, diccionario, compu)
                    window.UnHide()
                elif event == "Terminar Turno":
                    terminar_turno(turno, tabla, jugador, window, diccionario, config)
                elif event == "Reglas":
                    sg.Popup("Reglas")
                elif event == "pausa":
                    if sg.popup_ok_cancel('¿Pausar partida?', **estilo.tt) == "OK":
                        pausar(turno, jugador, compu, tabla, window, config, Jugador.bolsa)
                elif event == "top":
                    sg.popup("El top 10 de puntajes")
                elif event == "configuracion":
                    window.Hide()
                    t = configurar_dificultad(config, niveles, Jugador.bolsa, tiempo, act_config)
                    if t is not None:
                        tiempo = t
                    window.UnHide()
                    print("act config: ", act_config)
                elif event == "Configuración actual":
                    sg.Popup('''Configuración: \n
                        Nivel: {0} \n
                        Dificultad computadora: {1} \n
                        Cantidad de fichas: {2} \n
                        Puntaje de fichas: {3} \n
                        Tablero: {4} \n
                        Tiempo: {5} \n
                        Tipos de palabras: {6} \n'''.format(act_config[0], act_config[1], act_config[2], act_config[3],
                                                            act_config[4], str(act_config[5]), act_config[6]))
                elif event == "palabras":
                    sg.Popup(turno.get_lista_palabras(), **estilo.tt)
                elif event == "Terminar Partida":
                    if sg.popup_ok_cancel('¿Terminar partida?', **estilo.tt) == "OK":
                        terminar_partida(jugador, compu, window, config)
            elif not turno.es_turno_usuario():
                # -------
                #         SI YA NO ES EL TURNO DEL USUARIO
                # -------
                turno_compu(turno, tabla, compu, window, config, diccionario)
        # ------
        #       Condición de fin: si no hay mas fichas
        # ------
        elif jugador.get_cant_bolsa() == 0 or tiempo == 0:
            terminar_partida(jugador, compu, window, config)
            break
