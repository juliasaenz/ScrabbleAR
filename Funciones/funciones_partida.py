""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from Funciones.Ventanas_secundarias import ventana_shuffle
import PySimpleGUI as sg
import json


def letra_actual(event, turno, jugador):
    """ La letra del atril seleccionada por el usuario """
    turno.set_letra_actual(jugador.get_atril()[int(event)])
    turno.set_pos_actual(event)
    #print("Letra actual: ", turno.get_letra_actual())


def poner_ficha(event, turno, tabla, window):
    """ Ubica una ficha en el tablero """
    #print("Casillero no bloqueado: ", event)
    turno.agregar_casillero(event)
    turno.set_letras(turno.get_letra_actual())
    turno.add_atril_usada(turno.get_pos_actual())
    tabla.actualizar_casillero(turno.get_letra_actual(), event)
    window.FindElement(event).Update(turno.get_letra_actual())
    window.FindElement(turno.get_pos_actual()).Update(disabled=True)


def shuffle(turno, tabla, jugador, window, config, diccionario, compu):
    """ Cambia todas las fichas del atril y saltea el turno """
    # esto se puede hacer solo tres veces en la partida
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
    """ La computadora elige la mejor palabra posible y la posiciona en un lugar aleatorio"""
    window.Read(timeout=1)
    # -- Arma la palabra
    compu.jugada(tabla, diccionario, config, turno.get_primer_turno())
    if turno.get_primer_turno():
        turno.jugue_primer_turno()
    # -- Busca donde dibujarla y la dibuja
    i = 0
    for pos in compu.get_casilleros():
        tabla.actualizar_casillero(compu.get_palabra()[i], pos)
        window.FindElement(pos).Update(compu.get_palabra()[i], button_color=("#FAFAFA", "#4B3588"))
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
                window.FindElement(tupla).Update(button_color=("#FAFAFA", "#D92335"))
            #print("Puntaje jugador: ", jugador.get_puntaje())
            tabla.bloquear_casilleros(turno.get_casilleros_usados())
            jugador.fin_de_turno(turno.definir_puntos(tabla.get_matriz(), config["puntos"]), turno.get_atril_usadas())
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


def terminar_partida(jugador, compu, window, config):
    jugador.terminar_partida(config["puntos"])
    compu.terminar_partida(config["puntos"])
    score = 'PUNTAJE FINAL \n {}: {} puntos \n {}: {} puntos'.format(jugador.get_nombre(), jugador.get_puntaje(),
                                                                     compu.get_nombre(), compu.get_puntaje())
    sg.Popup(score)
    window.close()


def pausar(turno, jugador, compu, tabla, window, config, bolsa):
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
        "bolsa": bolsa,
        "nivel": config,
        "tablero": tabla.pausar_partida()
    }
    json.dump(juego, archivo, ensure_ascii=False, indent=4)
    archivo.close()
    window.close()
