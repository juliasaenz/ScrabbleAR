""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

# from nue_inicio import*
import random
from Funciones.funciones_partida import *
from Funciones.Ventanas_secundarias import *
from Inicio import correr_inicio, correr_tutorial

if correr_tutorial():
    # Inicio
    try:
        window, config, tiempo, Jugador, turno, jugador, compu, diccionario, act_config, continuar, tabla, niveles = correr_inicio()
    except TypeError:
        tiempo = -1
    # Quien Empieza
    try:
        if not continuar:
            turno.set_turno_usuario(bool(random.getrandbits(1)))
    except NameError:
        print("Se cerró en la ventana de Tutorial")
else:
    tiempo = -1

# -------------------------------------------
#                  JUEGO
# -------------------------------------------

# Tiempo es -1 cuando se cerro la ventana de Tutorial o Inicio
if tiempo != -1:
    while True:
        # --- Timer
        window["tiempo"].update('{}'.format(int(tiempo / 100)))
        window["bolsa"].update('{}'.format("Fichas restantes: {}".format(len(Jugador.bolsa))))
        tiempo = tiempo - 1

        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            sg.Popup("Se cerró la aplicación. \n Gracias por usar ScrabbleAR")
            break
        # ----- SI ES EL TURNO DEL USUARIO Y NO TERMINO LA PARTIDA
        if jugador.get_cant_bolsa() != 0 and tiempo != 0:
            if turno.es_turno_usuario():
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
                    letra_actual(event, turno, jugador, window)
                # --- Limpiar letras en el tablero
                elif event == "Limpiar":
                    limpiar(turno, tabla, window)
                # --- Elige que letras intercambiar y pasa de turno
                elif event == "Shuffle":
                    window.Hide()
                    shuffle(turno, tabla, jugador, window)
                    window.UnHide()
                    window.FindElement("turno").Update("Computadora")
                    turno_compu(turno, tabla, compu, window, config, diccionario)
                    window.FindElement("turno").Update(jugador.get_nombre())
                # --- Si la palabra es correcta, termina el turno
                elif event == "Terminar Turno":
                    terminar_turno(turno, tabla, jugador, window, diccionario, config)
                # --- Muestra las reglas del juego
                if event == "Reglas":
                    sg.Popup('''
                    Este es un juego basado en el Scrabble. \n
                    - Cada jugador debe formar palabras con las letras de su atril para conseguir
                    la mayor cantidad de puntos posibles. 
                    - El juego continua hasta que no haya más fichas o hasta que se termine el tiempo.
                    - El jugador con mayor puntaje al final de la partida será el ganador.
                    - El tablero cuenta con casilleros especiales que pueden sumar o restar puntos.
                    - Durante la partida el jugador podrá usar el Shuffle para cambiar una o más de las 
                    fichas en el atril, pero también perderá ese turno.
                    - En cualquier momento el jugador puede elegir Pausar la partida, esto cerrará la partida
                    ''', title="Reglas", **estilo.tt)
                # --- Si el usuario quiere, guarda la partida
                elif event == "pausa":
                    if sg.popup_ok_cancel('¿Guardar partida? \n Se cerrará la partida y podrás continuar luego',
                                          **estilo.tt) == "OK":
                        if turno.get_primer_turno():
                            sg.Popup("No se puede guardar la partida sin haber jugado por lo menos un turno",
                                     **estilo.tt)
                        else:
                            pausar(turno, jugador, compu, tabla, window, config, Jugador.bolsa, act_config)
                            terminar_partida(jugador, compu, window, config, act_config[0])
                            Jugador.bolsa.clear()
                            try:
                                reinicio_partida(window, config, tiempo, Jugador, turno, jugador, compu, diccionario,
                                                 act_config,
                                                 continuar, tabla, niveles)
                                window, config, tiempo, Jugador, turno, jugador, compu, diccionario, act_config, continuar, tabla, niveles = correr_inicio()
                            except TypeError:
                                break
                # --- Muestra el Top 10 de puntajes
                elif event == "top":
                    top_10()
                # --- Pausar partida
                elif event == "pp":
                    sg.Popup("Juego en pausa", **estilo.tt)
                # --- Accede a la configuración del nivel
                elif event == "configuracion":
                    window.Hide()
                    ant = config["tipos"].copy()
                    t = configurar_dificultad(config, niveles, Jugador.bolsa, tiempo, act_config)
                    # --- Actualizar tiempo, si es necesario
                    if t is not None:
                        tiempo = t
                    # --- Actualizar tablero, si es necesario
                    if config["tipos"] != ant:
                        for x in range(15):
                            for y in range(15):
                                if not tabla.esta_bloqueado((x, y)):
                                    tabla.actualizar_tipo((x, y), config["tipos"][x][y])
                                    window[(x, y)].update(button_color=("black", que_color(config["tipos"][x][y])))
                    window.UnHide()
                    window.FindElement("nivel").Update("NIVEL: {}".format(act_config[0].upper()))
                # --- Permite ver la configuración actual del nivel
                elif event == "Configuración actual":
                    sg.Popup('''Configuración: \n
                        Nivel: {0} \n
                        Dificultad computadora: {1} \n
                        Cantidad de fichas: {2} \n
                        Puntaje de fichas: {3} \n
                        Tablero: {4} \n
                        Tiempo: {5} \n
                        Tipos de palabras: {6} \n'''.format(act_config[0], act_config[1], act_config[2], act_config[3],
                                                            act_config[4], str(act_config[5]), act_config[6]),
                             **estilo.tt)
                # --- Muestra las palabras jugadas y el puntaje de cada una
                elif event == "palabras":
                    sg.Popup(turno.get_lista_palabras(), **estilo.tt)
                # --- Termina la partida
                elif event == "Terminar Partida":
                    if sg.popup_ok_cancel('¿Terminar partida?', **estilo.tt) == "OK":
                        terminar_partida(jugador, compu, window, config, act_config[0])
                        Jugador.bolsa.clear()
                        try:
                            reinicio_partida(window, config, tiempo, Jugador, turno, jugador, compu, diccionario,
                                             act_config, continuar, tabla, niveles)
                            window, config, tiempo, Jugador, turno, jugador, compu, diccionario, act_config, continuar, tabla, niveles = correr_inicio()
                        except TypeError:
                            break
            # --- Si ya no es el turno del usuario
            elif not turno.es_turno_usuario():
                window.FindElement("turno").Update("Computadora")
                turno_compu(turno, tabla, compu, window, config, diccionario)
                window.FindElement("turno").Update(jugador.get_nombre())
        # --- Si no hay más fichas o se acabo el tiempo, termina la partida
        elif jugador.get_cant_bolsa() == 0 or tiempo == 0:
            terminar_partida(jugador, compu, window, config, act_config[0])
            Jugador.bolsa.clear()
            try:
                reinicio_partida(window, config, tiempo, Jugador, turno, jugador, compu, diccionario, act_config,
                                 continuar, tabla, niveles)
                window, config, tiempo, Jugador, turno, jugador, compu, diccionario, act_config, continuar, tabla, niveles = correr_inicio()
            except TypeError:
                break
