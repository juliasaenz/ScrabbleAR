import json
import sys
from Clases.Tablero import Tablero
from Clases.Jugador import Jugador
from Funciones.funciones_palabras import palabra_es_valida, palabras_sin_tilde
from Funciones.diagrama import tutorial
import PySimpleGUI as sg

estado = "inicio"

# INICIO

# armo el diccionario de palabras válidas
diccionario = palabras_sin_tilde()

# abro el json del nivel que quiera
nivel = open("Archivos/nivel1", "r")
config = json.load(nivel)

# armo la bolsa de letras (es una lista)
bolsa = []
for letra in config["cantidad"].keys():
    for veces in range(config["cantidad"][letra]):
        bolsa.append(letra)

# abro el tutorial
# tutorial = tutorial()
# window = sg.Window("ScrabbleAR").Layout(tutorial)
# event, values = window.read()

jugador = Jugador("Julia", bolsa)

# paso a juego
# if event == None:
#    window.close()
# if event == "Jugar":
#   window.close()
tabla = Tablero()


def crear_boton():
    boton = []
    for x in range(15):
        for y in range(15):
            boton.append((x, y))
    return boton


# variables


elegir_direccion = True
movimientos = 0
letras_usadas = []
empezar = True
letra_act = " "
boton = crear_boton()
event_ant = None
matrix = []
x = 15
y = 15
for i in range(x):
    matrix.append([])
    for j in range(y):
        matrix[i].append(None)

# JUGAR
ventana_juego = [[sg.Frame(layout=tabla.dibujar(), title="Tablero")],
                 [],
                 [sg.Frame(layout=jugador.dibujar(), title="Atril de " + jugador.get_nombre())]
                 ]


###Funciones
def desbloquear_tablero():
    for x in range(15):
        for y in range(15):
            window.FindElement((x, y)).Update(disabled=False)
            window.FindElement((x, y)).Update(button_color=("black", "white"))


def bloquear_tablero(event):  # bloquea todo menos el evento
    for x in range(15):
        for y in range(15):
            if (x, y) != event:
                window.FindElement((x, y)).Update(disabled=True)
                window.FindElement((x, y)).Update(button_color=("black", "grey"))
    window.FindElement(event).Update(button_color=("black", "green4"))


def bloquear_casilla(event):  # bloquea una casilla #no
    if event != " ":
        window.FindElement(event).Update(button_color=("black", "grey"))
        window.FindElement(event).Update(disabled=True)

def desbloquear_casilla(event):  # desbloquea una casilla #no
    if event !=" ":
        window.FindElement(event).Update(button_color=("black", "green4"))
        window.FindElement(event).Update(disabled=False)


def bloquear_atril(letra):  # bloquea una letra
    window.FindElement(letra[0]).Update(button_color=("black", "grey"))
    window.FindElement(letra[0]).Update(disabled=True)


def desbloquear_atril(letra):  # desbloquea una letra
    window.FindElement(letra[0]).Update(button_color=("black", "white"))
    window.FindElement(letra[0]).Update(disabled=False)


def desbloquear_adyascentes(event):  # desbloquea los adyascentes del evento
    if event[1] < 14:
        window.FindElement((event[0], event[1] + 1)).Update(disabled=False)
        window.FindElement((event[0], event[1] + 1)).Update(button_color=("black", "green4"))
    if event[0] < 14:
        window.FindElement((event[0] + 1, event[1])).Update(disabled=False)
        window.FindElement((event[0] + 1, event[1])).Update(button_color=("black", "green4"))
    if event[0] > 0:
        window.FindElement((event[0] - 1, event[1])).Update(disabled=False)
        window.FindElement((event[0] - 1, event[1])).Update(button_color=("black", "green4"))


def intercambio():
    global matrix
    global event
    global letras_usadas
    global letra_act
    global event_ant
    if letra_act!=" ":
        letras_usadas.remove(matrix[event[0]][event[1]])
        desbloquear_atril(matrix[event[0]][event[1]])
        bloquear_atril(letra_act)
        matrix[event[0]][event[1]] = letra_act
        letras_usadas.append(letra_act)
        window.FindElement(event).Update(letra_act)
        letra_act = " "
        event_ant = event

def is_empty(data_structure): #lo uso para informar si la lista de letras usadas esta vacia
    if data_structure:
        return False
    else:
        return True




def bloqueo_desbloqueo_horientacion(event, event_ant):
    if event[0] == event_ant[0] - 1:  # bloquea y desbloquea los casilleros cuando elijo la orientacion hacia arriba
        if event_ant[1] < 14:
            bloquear_casilla((event_ant[0], event_ant[1] + 1))
        if event_ant[0] < 14:
            bloquear_casilla((event_ant[0] + 1, event_ant[1]))
        if event[0] > 0:
            desbloquear_casilla((event[0] - 1, event[1]))

    if event[0] == event_ant[0] + 1:  # bloquea y desbloquea los casilleros cuando elijo la orientacion hacia abajo
        if event_ant[0] > 0:
            bloquear_casilla((event_ant[0] - 1, event_ant[1]))
        if event_ant[1] < 14:
            bloquear_casilla((event_ant[0], event_ant[1] + 1))
        if event[0] < 14:
            desbloquear_casilla((event[0] + 1, event[1]))

    if event[1] == event_ant[1] + 1:  # bloquea y desbloquea los casilleros cuando elijo la orientacion horizontal
        if event_ant[0] > 0:
            bloquear_casilla((event_ant[0] - 1, event_ant[1]))
        if event_ant[0] < 14:
            bloquear_casilla((event_ant[0] + 1, event_ant[1]))
        if event[1] < 14:
            desbloquear_casilla((event[0], event[1] + 1))


window = sg.Window("ScrabbleAR").Layout(ventana_juego)

while True:
    event, values = window.read()
    if (event == None):
        break

    if event in diccionario and is_empty(letras_usadas):
        letra_act = event
        desbloquear_tablero()
        empezar = False
    if event in diccionario and empezar == False:
        letra_act = event

    if (event in boton):
        if matrix[event[0]][event[1]] in letras_usadas:
            if letra_act!=" ":
                intercambio()  # cambia las letras en matrix y tablero,bloquea atril y desbloquea atril, tambien saca de letras_usadas la letra recuperada y guarda en letras_usadas la intercambiada, para colmo actualiza el evento anterior
            else:
                letras_usadas.remove(matrix[event[0]][event[1]])
                desbloquear_atril(matrix[event[0]][event[1]])
                window.FindElement(event).Update(letra_act)
                matrix[event[0]][event[1]] =None
                event_ant = event
                if (is_empty(letras_usadas)):
                    desbloquear_tablero()

        else:
            if elegir_direccion and event_ant != None and letra_act != " ":  # ingresa la segunda vez q pones una letra
                bloqueo_desbloqueo_horientacion(event, event_ant)
                matrix[event[0]][event[1]] = letra_act
                window.FindElement(event).Update(letra_act) # no
                letras_usadas.append(letra_act)
                bloquear_atril(letra_act)
                event_ant = event
                letra_act = " "

            if event_ant is None and letra_act!= " ":  # aca ingresa la primera vez q pones una letra
                window.FindElement(event).Update(letra_act)#no
                matrix[event[0]][event[1]] = letra_act
                bloquear_tablero(event)
                desbloquear_adyascentes(event)
                letras_usadas.append(letra_act)
                bloquear_atril(letra_act)
                event_ant = event
                letra_act = " "

