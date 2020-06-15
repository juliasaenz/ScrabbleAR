import json
import sys
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
    if (event == "Jugar"):
        window.close()

        #NIVEL----
        nivel = open("Archivos/nivel1", "r")
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

        ventana_juego = [[sg.Frame(layout=compu.dibujar(),key = compu.get_nombre(),
                                   title = "Atril de " + jugador.get_nombre()),sg.Text("Puntaje: "+ str(compu.get_puntaje()),key = "p_compu")],
                        [sg.Frame(layout=tabla.dibujar(), title="Tablero"),sg.Text("Tiempo: 60", key = "tiempo")],
                         [],
                         [sg.Frame(layout=jugador.dibujar(), key=jugador.get_nombre(),
                                   title="Atril de " + jugador.get_nombre()),
                          sg.Button("Shuffle"), sg.Ok("Terminar Turno"),sg.Text("Puntaje: "+ str(compu.get_puntaje()),key = "p_jugador")]
                         ]
        window = sg.Window("ScrabbleAR").Layout(ventana_juego)

        turno = Turno()
        while True:
            event, values = window.read()
            # ----- SI ES EL TURNO DEL USUARIO -----
            if(turno.es_turno_usuario()):
                # CUENTA REGRESIVA
                #turno.countdown()
                print("event: ",event)
                if(event == None):
                    break
                # --- si toco un boton del tablero
                elif (event in tabla.get_posiciones()):
                    #si el casillero no esta bloqueado
                    if(not tabla.esta_bloqueado(event)):
                        #si el casillero esta vacio
                        if(tabla.get_casillero(event) == ""):
                            print("Casillero no bloqueado: ",event)
                            turno.agregar_casillero(event)
                            turno.set_letras(turno.get_letra_actual())
                            tabla.actualizar_casillero(turno.get_letra_actual(),event)
                            window.FindElement(event).Update(turno.get_letra_actual())
                            window.FindElement(turno.get_pos_actual()).Update(disabled=True)
                    #actualizo letra actual
                    turno.set_letra_actual("")
                # --- si toco un boton del atril
                elif (event in "0123456"):
                    turno.set_letra_actual(jugador.get_atril()[int(event)])
                    turno.set_pos_actual(event)
                    print("Letra actual: ",turno.get_letra_actual())
                elif (event == "Shuffle"):
                    #esto se puede hacer solo tres veces en la partida
                    if( jugador.shuffle() >= 0):
                        i = 0
                        for dato in jugador.get_atril():
                            window.FindElement(str(i)).Update(dato)
                            i = i + 1
                        tabla.limpiar_matriz()
                        for i in range (7):
                            window.FindElement(str(i)).Update(disabled=True)
                        for pos in turno.get_casilleros_usados():
                            window.FindElement(pos).Update("")
                        turno.reinicio()
                    # se reinicia el turno
                    if (jugador.get_cambios() == 0):
                        window.FindElement("Shuffle").Update(disabled =True)
                elif(event == "Terminar Turno"):
                    resultado = turno.evaluar_palabra(tabla.get_matriz(),diccionario,config)
                    #si la palabra no es válida
                    if(resultado == 100):
                        print("Palabra equivocada!!")
                        sg.Popup("Esa palabra no es válida :(")
                        tabla.limpiar_matriz()
                        for i in range (7):
                            window.FindElement(str(i)).Update(disabled=False)
                        for pos in turno.get_casilleros_usados():
                            window.FindElement(pos).Update("")
                        turno.limpiar()
                    else:
                    #si la palabra es válida
                        tabla.bloquear_casilleros(turno.get_casilleros_usados())
                        for tupla in turno.get_casilleros_usados():
                            window.FindElement(tupla).Update(button_color= ("white", "black"))
                        jugador.actualizar_puntaje(turno.definir_puntos(tabla.get_matriz(),config["puntos"]))
                        jugador.sacar_fichas(turno.get_letras())
                        jugador.reponer_atril()
                        for i in range (7):
                            window.FindElement(str(i)).Update(jugador.get_ficha(i), disabled=True)
                        window.FindElement("p_jugador").Update("Puntaje: " + str(jugador.get_puntaje()))
                        turno.reinicio()
                        print("Muy bien! Palabra correcta!")

            # ------- SI YA NO ES EL TURNO DEL USUARIO ---------- #
            else:
                print("Es el turno de la compu")
                # -- Arma la palabra
                compu.armar_palabra(diccionario, config["palabras"])
                # -- Busca donde dibujarla y la dibuja
                i = 0
                for pos in compu.ubicar_palabra(tabla):
                    tabla.actualizar_casillero(compu.get_palabra()[i],pos)
                    window.FindElement(pos).Update(compu.get_palabra()[i],button_color=("white", "black"))
                    i = i + 1
                # ---
                tabla.bloquear_casilleros(compu.get_casilleros())
                compu.actualizar_puntaje(compu.definir_puntos(tabla.get_matriz(),config["puntos"]))
                print("puntaje compu: ",str(compu.get_puntaje()))
                window.FindElement("p_compu").Update("Puntaje: " + str(compu.get_puntaje()))
                compu.sacar_y_reponer_atril()
                turno.reinicio()
                for i in range(7):
                    window.FindElement(str(i)).Update(disabled=False)


