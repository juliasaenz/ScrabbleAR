""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from Funciones.Ventanas_secundarias import ventana_shuffle
from Funciones.leaderboard import guardar_partida
import PySimpleGUI as sg
import estilo
import json


def letra_actual(event, turno, jugador):
    """ La letra del atril seleccionada por el usuario """
    turno.set_letra_actual(jugador.get_atril()[int(event)])
    turno.set_pos_actual(event)


def poner_ficha(event, turno, tabla, window):
    """ Ubica una ficha en el tablero """
    turno.agregar_casillero(event)
    turno.set_letras(turno.get_letra_actual())
    turno.add_atril_usada(turno.get_pos_actual())
    tabla.actualizar_casillero(turno.get_letra_actual(), event)
    window.FindElement(event).Update(turno.get_letra_actual())
    window.FindElement(turno.get_pos_actual()).Update(disabled=True)


def shuffle(turno, tabla, jugador, window, config, diccionario, compu):
    """ Cambia las fichas del atril seleccionadas por el usuario y saltea el turno,
    se puede hacer 3 veces por partida """
    a_cambiar = ventana_shuffle(jugador.get_atril())
    if len(a_cambiar) > 0:
        jugador.shuffle(a_cambiar)
        i = 0
        for dato in jugador.get_atril():
            window.FindElement(str(i)).Update(dato)
            i = i + 1
        tabla.limpiar_matriz()
        for i in range(7):
            window.FindElement(str(i)).Update(disabled=True)
        for pos in turno.get_casilleros_usados():
            window.FindElement(pos).Update("")
        turno.reinicio(jugador.get_nombre())
        turno_compu(turno, tabla, compu, window, config, diccionario)
    # se reinicia el turno
    if jugador.get_cambios() == 0:
        window.FindElement("Shuffle").Update(disabled=True)


def turno_compu(turno, tabla, compu, window, config, diccionario):
    """ La computadora elige palabra y la posiciona según el nivel """
    window.Read(timeout=1)
    # -- Arma la palabra
    compu.jugada(tabla, diccionario, config, turno.get_primer_turno())
    if turno.get_primer_turno():
        turno.jugue_primer_turno()
    # -- La posiciona en el tablero
    i = 0
    for pos in compu.get_casilleros():
        tabla.actualizar_casillero(compu.get_palabra()[i], pos)
        window.FindElement(pos).Update(compu.get_palabra()[i], button_color=("#FAFAFA", "#06586A"))
        i = i + 1
    # ---
    tabla.bloquear_casilleros(compu.get_casilleros())
    compu.actualizar_puntaje(compu.definir_puntos(tabla.get_matriz(), config["puntos"], compu.get_casilleros()))
    window.FindElement("p_compu").Update(str(compu.get_puntaje()))
    turno.set_palabra(compu.get_palabra())
    turno.set_puntaje(compu.get_puntaje_palabra())
    compu.sacar_y_reponer_atril()
    turno.reinicio(compu.get_nombre())
    for i in range(7):
        window.FindElement(str(i)).Update(disabled=False)


def limpiar(turno, tabla, window):
    """ Saca las fichas del tablero y las vuelve a activar en el atril """
    for pos in turno.get_casilleros_usados():
        window.FindElement(pos).Update("")
    tabla.limpiar_matriz()
    turno.limpiar()
    for i in range(7):
        window.FindElement(str(i)).Update(disabled=False)


def terminar_turno(turno, tabla, jugador, window, diccionario, config):
    """ Si la palabra es correcta pasa al turno de la compy, sino limpia el tablero"""
    resultado = turno.evaluar_palabra(tabla.get_matriz(), diccionario, config)
    if turno.validar_turno():
        # si la palabra no es válida
        if resultado == 100:
            # print("Palabra equivocada!!")
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
                window.FindElement(tupla).Update(button_color=("#FAFAFA", "#6A0642"))
            # print("Puntaje jugador: ", jugador.get_puntaje())
            tabla.bloquear_casilleros(turno.get_casilleros_usados())
            jugador.fin_de_turno(turno.definir_puntos(tabla.get_matriz(), config["puntos"]), turno.get_atril_usadas(),
                                 turno.get_casilleros_usados())
            window.FindElement("p_jugador").Update(str(jugador.get_puntaje()))
            for i in range(7):
                window.FindElement(str(i)).Update(jugador.get_ficha(i), disabled=True)
            turno.reinicio(jugador.get_nombre())
            turno.jugue_primer_turno()
    else:
        tabla.limpiar_matriz()
        for i in range(7):
            window.FindElement(str(i)).Update(disabled=False)
        for pos in turno.get_casilleros_usados():
            window.FindElement(pos).Update("")
        sg.Popup("Una ficha debe estar en el casillero del medio")
        turno.limpiar()


def terminar_partida(jugador, compu, window, config, nivel):
    jugador.terminar_partida(config["puntos"])
    compu.terminar_partida(config["puntos"])

    score = """PUNTAJE FINAL \n {}: {} puntos \n {}: {} puntos""".format(jugador.get_nombre(),
                                                                         jugador.get_puntaje(),
                                                                         compu.get_nombre(), compu.get_puntaje())

    if jugador.get_puntaje() > compu.get_puntaje():
        sg.Popup(score + "\n\n ¡Ganaste! ¡Felicidades!", **estilo.tt)
        if sg.popup_yes_no("¿Guardar puntaje?", **estilo.tt):
            datos = jugador.guardar_partida(nivel)
            guardar_partida(datos)
            print("--------------------------------")
            print(datos)
    elif compu.get_puntaje() > jugador.get_puntaje():
        sg.Popup(score + "\n\n ¡Ganó la Computadora! ¡Mejor suerte la próxima!", **estilo.tt)
    else:
        sg.Popup(score + "\n\n ¡Es un empate!", **estilo.tt, **estilo.tt)
    window.close()


def pausar(turno, jugador, compu, tabla, window, config, bolsa, act_config):
    """ Guarda los datos de los jugadores, el trablero, la bolsa y el nivel en un archivo"""
    if turno.es_turno_usuario():
        for pos in turno.get_casilleros_usados():
            window.FindElement(pos).Update("")
        tabla.limpiar_matriz()
        turno.limpiar()
    sg.Popup("Partida Guardada", **estilo.tt)
    archivo = open("Archivos/ultima_partida.txt", "w", encoding="utf-8")
    juego = {
        "jugador": jugador.pausar_turno(),
        "compu": compu.pausar_turno(),
        "bolsa": bolsa,
        "nivel": config,
        "tablero": tabla.pausar_partida(),
        "palabras_jugadas": turno.guardar_lista_palabras(),
        "act_config": act_config,
        "turno": turno.es_turno_usuario()
    }
    json.dump(juego, archivo, ensure_ascii=False, indent=4)
    archivo.close()
    window.close()


def que_color(tipo):
    """ Recibe un String con el tipo de casillero y devuelve el color correspondiente """
    if tipo == "doble_letra":
        return "#75E540"
    elif tipo == "triple_letra":
        return "#E5CB40"
    elif tipo == "doble_palabra":
        return "#E59940"
    elif tipo == "triple_palabra":
        return "#E54040"
    elif tipo == "menos_uno":
        return "#40E5E5"
    elif tipo == "menos_dos":
        return "#4078E5"
    elif tipo == "menos_tres":
        return "#E540DE"
    else:
        return "#FAFAFA"


def top_10():
    try:
        leaderboard = open("Archivos/leaderboard", "r", encoding="utf-8")
        partidas = json.load(leaderboard)
        leaderboard.close()
        lista_10 = "TOP 10: \n"
        i = 1
        for juego in partidas.values():
            texto = "{0}: {1}  -  Puntaje: {2}  -  Fecha: {3}  -  Nivel: {4}".format(str(i), juego['nombre'], juego['puntaje'],
                                                                         juego['fecha'], juego['nivel'])
            i = i + 1
            lista_10 = lista_10 + "\n\n" + texto
        sg.Popup(lista_10, **estilo.tt)
    except FileNotFoundError:
        sg.Popup("Todavia no se guardó ninguna partida", **estilo.tt)
