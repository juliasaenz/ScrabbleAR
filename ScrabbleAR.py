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


turno = Turno()
tiempo = config["tiempo"]*100

def timer():
    ''' Actualiza el temporizador '''
    global tiempo
    tiempo = tiempo - 1
    # --------- Display timer in window --------
    window["tiempo"].update('Tiempo: {}'.format(int(tiempo/100)))
def letra_actual(event):
    ''' La letra del atril seleccionada por el usuario '''
    turno.set_letra_actual(jugador.get_atril()[int(event)])
    turno.set_pos_actual(event)
    print("Letra actual: ", turno.get_letra_actual())
def turno_compu():
    ''' La computadora elige la mejor palabra posible y la posiciona en un lugar aleatorio'''
    window.Read(timeout=1)
    # -- Arma la palabra
    compu.jugada(tabla, diccionario, config)
    # -- Busca donde dibujarla y la dibuja
    i = 0
    for pos in compu.get_casilleros():
        tabla.actualizar_casillero(compu.get_palabra()[i], pos)
        window.FindElement(pos).Update(compu.get_palabra()[i], button_color=("white", "black"))
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
    ''' Saca las fichas del tablero y las vuelve a activar en el atril '''
    for pos in turno.get_casilleros_usados():
        window.FindElement(pos).Update("")
    tabla.limpiar_matriz()
    turno.limpiar()
    for i in range(7):
        window.FindElement(str(i)).Update(disabled=False)
def pausar():
    ''' Guarda los datos de los jugadores, el trablero, la bolsa y el nivel en un archivo'''
    if (turno.es_turno_usuario()):
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
def poner_ficha(event):
    ''' Ubica una ficha en el tablero '''
    print("Casillero no bloqueado: ", event)
    turno.agregar_casillero(event)
    turno.set_letras(turno.get_letra_actual())
    turno.add_atril_usada(turno.get_pos_actual())
    tabla.actualizar_casillero(turno.get_letra_actual(), event)
    window.FindElement(event).Update(turno.get_letra_actual())
    window.FindElement(turno.get_pos_actual()).Update(disabled=True)
def shuffle(event):
    ''' Cambia todas las fichas del atril y saltea el turno '''
    # esto se puede hacer solo tres veces en la partida
    if (jugador.shuffle() >= 0):
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
    if (jugador.get_cambios() == 0):
        window.FindElement("Shuffle").Update(disabled=True)
def terminar_turno(event):
    ''' Si la palabra es correcta pasa al turno de la compy, sino limpia el tablero'''
    resultado = turno.evaluar_palabra(tabla.get_matriz(), diccionario, config)
    # si la palabra no es válida
    if (resultado == 100):
        print("Palabra equivocada!!")
        sg.popup_timed("No es una palabra válida",background_color="black")
        tabla.limpiar_matriz()
        for i in range(7):
            window.FindElement(str(i)).Update(disabled=False)
        for pos in turno.get_casilleros_usados():
            window.FindElement(pos).Update("")
        turno.limpiar()
    else:
        # si la palabra es válida
        for tupla in turno.get_casilleros_usados():
            window.FindElement(tupla).Update(button_color=("white", "black"))
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

#-------------
#          JUEGO
#-------------

while True:
    timer()
    event, values = window.read(timeout=10)
    # ----- SI ES EL TURNO DEL USUARIO Y NO TERMINO LA PARTIDA
    if (jugador.get_cant_bolsa() != 0 and turno.es_turno_usuario()):
        if(event != "__TIMEOUT__"):
            print("event: ", event)
        if (event == None):
            break
        # --- si toco un boton del tablero
        elif (event in tabla.get_posiciones()):
            if(turno.get_letra_actual() != ""):
                # si el casillero no esta bloqueado
                if (not tabla.esta_bloqueado(event)):
                    # si el casillero esta vacio
                    if (tabla.get_casillero(event) == ""):
                        poner_ficha(event)
                # actualizo letra actual
                turno.set_letra_actual("")
                turno.set_pos_actual("")
        # --- si toco un boton del atril
        elif (event in "0123456"):
            letra_actual(event)
        elif (event == "Limpiar"):
            limpiar()
        elif (event == "Shuffle"):
            shuffle(event)
        elif (event == "Terminar Turno"):
            terminar_turno(event)
        elif (event == "Reglas"):
            sg.Popup("Reglas")
        elif (event == "pausa"):
            pausar()
    if(tiempo == 0):
        limpiar()
        turno_compu()
    # ------
    #       Condición de fin: si no hay mas fichas
    # ------
    elif (jugador.get_cant_bolsa() == 0):
        ganador = max(jugador.get_puntaje(), compu.get_puntaje())
        if (jugador.get_puntaje() > compu.get_puntaje()):
            nom = jugador.get_nombre()
        else:
            nom = compu.get_nombre()
        sg.popup("Se terminó la partida y ganó ", nom)
        window.close()