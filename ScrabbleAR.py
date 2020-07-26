""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from Inicio import*

# -------------------------------------------
#                  JUEGO
# -------------------------------------------

# Quien empieza
turno.set_turno_usuario(bool(random.getrandbits(1)))

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
                # --- Limpiar letras en el tablero
                elif event == "Limpiar":
                    limpiar(turno, tabla, window)
                # --- Elige que letras intercambiar y pasa de turno
                elif event == "Shuffle":
                    window.Hide()
                    shuffle(turno, tabla, jugador, window, config, diccionario, compu)
                    window.UnHide()
                # --- Si la palabra es correcta, termina el turno
                elif event == "Terminar Turno":
                    terminar_turno(turno, tabla, jugador, window, diccionario, config)
                # --- Muestra las reglas del juego
                elif event == "Reglas":
                    sg.Popup("Reglas")
                # --- Si el usuario quiere, guarda la partida
                elif event == "pausa":
                    if sg.popup_ok_cancel('¿Pausar partida?', **estilo.tt) == "OK":
                        pausar(turno, jugador, compu, tabla, window, config, Jugador.bolsa)
                # --- Muestra el Top 10 de puntajes
                elif event == "top":
                    sg.popup("El top 10 de puntajes")
                # --- Accede a la configuración del nivel
                elif event == "configuracion":
                    window.Hide()
                    t = configurar_dificultad(config, niveles, Jugador.bolsa, tiempo, act_config)
                    if t is not None:
                        tiempo = t
                    window.UnHide()
                    print("act config: ", act_config)
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
                                                            act_config[4], str(act_config[5]), act_config[6]))
                # --- Muestra las palabras jugadas y el puntaje de cada una
                elif event == "palabras":
                    sg.Popup(turno.get_lista_palabras(), **estilo.tt)
                # --- Termina la partida
                elif event == "Terminar Partida":
                    if sg.popup_ok_cancel('¿Terminar partida?', **estilo.tt) == "OK":
                        terminar_partida(jugador, compu, window, config)
            # --- Si ya no es el turno del usuario
            elif not turno.es_turno_usuario():
                turno_compu(turno, tabla, compu, window, config, diccionario)
        # --- Si no hay más fichas o se acabo el tiempo, termina la partida
        elif jugador.get_cant_bolsa() == 0 or tiempo == 0:
            terminar_partida(jugador, compu, window, config)
            break
