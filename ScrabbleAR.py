import json
import estilo
from Clases.Tablero import Tablero
from Clases.Jugador import Jugador
from Clases.Computadora import Computadora
from Clases.Turno import Turno
from Funciones.funciones_palabras import palabras_sin_tilde
from Funciones.Ventanas_extra import tutorial, inicio
from Funciones.Niveles import actualizar_todo_dicc
import PySimpleGUI as sg

# ------ TUTORIAL
tutorial = tutorial()
window = sg.Window("ScrabbleAR").Layout(tutorial)
event, values = window.read()

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
        if len(values[1]) == 0:
            config = {
                "puntos": niveles["puntos"]["fácil"]["fácil"],
                "tiempo": niveles["tiempo"]["fácil"],
                "cantidad": niveles["letras"]["fácil"]["fácil"],
                "palabras": niveles["palabras"]["fácil"],
                "tipos": niveles["tipos"]["fácil"],
                "compu": niveles["compu"]["fácil"]
            }
        else:
            config = {
                "puntos": niveles["puntos"][values[1][0]][values[1][0]],
                "tiempo": niveles["tiempo"][values[1][0]],
                "cantidad": niveles["letras"][values[1][0]][values[1][0]],
                "palabras": niveles["palabras"][values[1][0]],
                "tipos": niveles["tipos"][values[1][0]],
                "compu": niveles["compu"][values[1][0]]
            }

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

    ventana_juego = [[sg.Button("Reglas", button_color=("#FAFAFA", "#151514"), **estilo.tt),
                      sg.Button("Top Ten Puntajes", key="top", button_color=("#FAFAFA", "#151514"), **estilo.tt),
                      sg.Button("Pausar Partida", key="pausa", button_color=("#FAFAFA", "#151514"), **estilo.tt),
                      sg.Button("Configuración", key="configuracion", button_color=("#FAFAFA", "#151514"),
                                **estilo.tt)],
                     [sg.Frame(layout=compu.dibujar(), key=compu.get_nombre(),
                               title="Atril de " + compu.get_nombre(), **estilo.tt), sg.Text("Puntaje: ", **estilo.tt),
                      sg.Text("  0  ", key="p_compu", **estilo.tt)],
                     [sg.Frame(layout=tabla.dibujar(), title="Tablero", **estilo.tt),
                      sg.Text('Tiempo: {}'.format(config["tiempo"]), key="tiempo", **estilo.tt)],
                     [],
                     [sg.Frame(layout=jugador.dibujar(), key=jugador.get_nombre(),
                               title="Atril de " + jugador.get_nombre(), **estilo.tt),
                      sg.Button("Shuffle", button_color=("#FAFAFA", "#151514"), **estilo.tt),
                      sg.Button("Limpiar", button_color=("#FAFAFA", "#151514"), **estilo.tt),
                      sg.Ok("Terminar Turno", button_color=("#FAFAFA", "#151514"), **estilo.tt),
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
    # --------- Display timer in window --------
    window["tiempo"].update('Tiempo: {}'.format(int(tiempo / 100)))


def letra_actual():
    """ La letra del atril seleccionada por el usuario """
    turno.set_letra_actual(jugador.get_atril()[int(event)])
    turno.set_pos_actual(event)
    print("Letra actual: ", turno.get_letra_actual())


def turno_compu():
    """ La computadora elige la mejor palabra posible y la posiciona en un lugar aleatorio"""
    window.Read(timeout=1)
    # -- Arma la palabra
    compu.jugada(tabla, diccionario, config)
    # -- Busca donde dibujarla y la dibuja
    i = 0
    for pos in compu.get_casilleros():
        tabla.actualizar_casillero(compu.get_palabra()[i], pos)
        window.FindElement(pos).Update(compu.get_palabra()[i], button_color=("#FAFAFA", "#4B3588"))
        i = i + 1
    # ---
    tabla.bloquear_casilleros(compu.get_casilleros())
    compu.actualizar_puntaje(compu.definir_puntos(tabla.get_matriz(), config["puntos"]))
    print("puntaje compu: ", str(compu.get_puntaje()))
    window.FindElement("p_compu").Update(str(compu.get_puntaje()))
    compu.sacar_y_reponer_atril()
    turno.reinicio()
    for i in range(7):
        window.FindElement(str(i)).Update(disabled=False)


def limpiar():
    """ Saca las fichas del tablero y las vuelve a activar en el atril """
    for pos in turno.get_casilleros_usados():
        window.FindElement(pos).Update("")
    tabla.limpiar_matriz()
    turno.limpiar()
    for i in range(7):
        window.FindElement(str(i)).Update(disabled=False)


def pausar():
    """ Guarda los datos de los jugadores, el trablero, la bolsa y el nivel en un archivo"""
    if turno.es_turno_usuario():
        for pos in turno.get_casilleros_usados():
            window.FindElement(pos).Update("")
        tabla.limpiar_matriz()
        turno.limpiar()
    sg.Popup("Partida Guardada")
    archivo = open("ultima_partida.txt", "w", encoding="utf-8")
    juego = {
        "jugador": jugador.pausar_turno(),
        "compu": compu.pausar_turno(),
        "bolsa": Jugador.bolsa,
        "nivel": config,
        "tablero": tabla.pausar_partida()
    }
    json.dump(juego, archivo, ensure_ascii=False, indent=4)
    archivo.close()
    window.close()


def poner_ficha():
    """ Ubica una ficha en el tablero """
    print("Casillero no bloqueado: ", event)
    turno.agregar_casillero(event)
    turno.set_letras(turno.get_letra_actual())
    turno.add_atril_usada(turno.get_pos_actual())
    tabla.actualizar_casillero(turno.get_letra_actual(), event)
    window.FindElement(event).Update(turno.get_letra_actual())
    window.FindElement(turno.get_pos_actual()).Update(disabled=True)


def shuffle():
    """ Cambia todas las fichas del atril y saltea el turno """
    # esto se puede hacer solo tres veces en la partida
    if jugador.shuffle() >= 0:
        i = 0
        for dato in jugador.get_atril():
            window.FindElement(str(i)).Update(dato)
            i = i + 1
        tabla.limpiar_matriz()
        for i in range(7):
            window.FindElement(str(i)).Update(disabled=True)
        for pos in turno.get_casilleros_usados():
            window.FindElement(pos).Update("")
        turno.reinicio()
        turno_compu()
    # se reinicia el turno
    if jugador.get_cambios() == 0:
        window.FindElement("Shuffle").Update(disabled=True)


def terminar_turno():
    """ Si la palabra es correcta pasa al turno de la compy, sino limpia el tablero"""
    resultado = turno.evaluar_palabra(tabla.get_matriz(), diccionario, config)
    # si la palabra no es válida
    if resultado == 100:
        print("Palabra equivocada!!")
        sg.popup_timed("No es una palabra válida", background_color="black")
        tabla.limpiar_matriz()
        for i in range(7):
            window.FindElement(str(i)).Update(disabled=False)
        for pos in turno.get_casilleros_usados():
            window.FindElement(pos).Update("")
        turno.limpiar()
    else:
        # si la palabra es válida
        for tupla in turno.get_casilleros_usados():
            window.FindElement(tupla).Update(button_color=("#FAFAFA", "#D92335"))
        print("Puntaje jugador: ", jugador.get_puntaje())
        tabla.bloquear_casilleros(turno.get_casilleros_usados())
        jugador.fin_de_turno(turno.definir_puntos(tabla.get_matriz(), config["puntos"]), turno.get_atril_usadas())
        window.FindElement("p_jugador").Update(str(jugador.get_puntaje()))
        for i in range(7):
            window.FindElement(str(i)).Update(jugador.get_ficha(i), disabled=True)
        turno.reinicio()
        # -------
        #         SI YA NO ES EL TURNO DEL USUARIO
        # -------
        turno_compu()



def configurar_dificultad():
    lista = ["", "fácil", "medio", "difícil"]

    configurar = [[sg.Text("Dificultad Computadora: ", **estilo.tt), sg.Combo(lista, **estilo.tt)],
                  [sg.Text("Puntaje fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt), sg.Button("Configurar "
                                                                                                     "individualmente", key ="config_1", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Cantidad fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt), sg.Button("Configurar "
                                                                                                      "individualmente", key ="config_2", **estilo.tt,  button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Tablero: ", **estilo.tt), sg.Combo(lista, **estilo.tt)]
                  ]

    c_layout = [
                [sg.Text("Seleccionar nivel: ", **estilo.tt), sg.Combo(["fácil", "medio", "difícil"],**estilo.tt)],
                [sg.Frame(layout=configurar, title="Configuración manual")],
                [sg.Ok("Confirmar cambios", **estilo.tt,  button_color=("#FAFAFA", "#151514")), sg.Cancel("Cancelar", **estilo.tt,  button_color=("#FAFAFA", "#151514"))]
                ]

    c_window = sg.Window("Configuración", c_layout, **estilo.tt)
    while True:
        event2, values2 = c_window.Read()
        print("event2: ", event2, " values2: ", values2)
        if event2 == sg.WIN_CLOSED or event2 == "Cancelar":
            c_window.Close()
        elif event2 == "Confirmar cambios":
            if values2[0] is not None or values2[0] != "":
                actualizar_todo_dicc(config, niveles, values2[0])
            if values2[1] is not None or values2[1] != "":
                config["compu"] = niveles["compu"][values2[1]]
            if values2[2] is not None or values2[2] != "":
                config["puntos"] = niveles["compu"][values2[2]]
            if values2[3] is not None or values2[3] != "":
                config["cantidad"] = niveles["letras"][values2[3]]
            c_window.Close()
        elif event2 == "config_1":
            sg.popup("HELLO")
        elif event2 == "config_2":
            sg.popup("config")

        window.UnHide()
        break

    # -------------


#          JUEGO
# -------------

# Config
ventana_config = False

# Tiempo es -1 cuando se cerro la ventana de Tutorial o Inicio
if tiempo != -1:
    while True:
        timer()
        event, values = window.read(timeout=10)
        # ----- SI ES EL TURNO DEL USUARIO Y NO TERMINO LA PARTIDA
        if jugador.get_cant_bolsa() != 0 and turno.es_turno_usuario() and tiempo != 0:
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
                            poner_ficha()
                    # actualizo letra actual
                    turno.set_letra_actual("")
                    turno.set_pos_actual("")
            # --- si toco un boton del atril
            elif event in "0123456":
                letra_actual()
            elif event == "Limpiar":
                limpiar()
            elif event == "Shuffle":
                shuffle()
            elif event == "Terminar Turno":
                terminar_turno()
            elif event == "Reglas":
                sg.Popup("Reglas")
            elif event == "pausa":
                if sg.popup_ok_cancel('¿Pausar partida?') == "OK":
                    pausar()
            elif event == "top":
                sg.popup("El top 10 de puntajes")
            elif event == "configuracion":
                ventana_config = True
                window.Hide()
                configurar_dificultad()
                print("nivel: ",config["compu"])
        # ------
        #       Condición de fin: si no hay mas fichas
        # ------
        elif jugador.get_cant_bolsa() == 0 or tiempo == 0:
            ganador = max(jugador.get_puntaje(), compu.get_puntaje())
            if jugador.get_puntaje() > compu.get_puntaje():
                nom = 'Ganó ', jugador.get_nombre(), '. ¡Felicidades!'
            elif jugador.get_puntaje() > compu.get_puntaje():
                nom = 'Ganó ', compu.get_nombre(), '. ¡Mejor suerte la próxima!'
            else:
                nom = '¡Fue un empate!'
            sg.Popup(nom)
            window.close()
            break
