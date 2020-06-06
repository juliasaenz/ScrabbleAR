import json
import sys
from Clases.Tablero import Tablero
from Clases.Jugador import Jugador
from Funciones.funciones_palabras import palabra_es_valida, palabras_sin_tilde
from Funciones.diagrama import tutorial
import PySimpleGUI as sg

estado = "inicio"

# INICIO

# este diccionario se usa para las letras del atril, no para validar palabras y para saber si el evento seleccionado
# es una letra que se debe de poner en el tablero
diccionario = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v", "w", "x", "y", "z"}

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

orientacion = " "
letras_usadas = []
segunda_letra = False
primera_letra = True
letra_act = " "
boton = crear_boton()
event_ant = None
matrix = []


def reinicio_matrix():
    global matrix
    x = 15
    y = 15
    for i in range(x):
        matrix.append([])
        for j in range(y):
            matrix[i].append(None)


reinicio_matrix()
# JUGAR
ventana_juego = [[sg.Frame(layout=tabla.dibujar(), title="Tablero")],
                 [],
                 [sg.Frame(layout=jugador.dibujar(), title="Atril de " + jugador.get_nombre())]
                 ]


# -------------------------------------------------------------------------------------------------------------------- #
#                                               Funciones                                                              #
# -------------------------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
#                           Funciones Atril                              #
# ---------------------------------------------------------------------- #
def bloquear_atril(letra):
    """Bloquea la letra enviada del atril"""
    window.FindElement(letra[0]).Update(button_color=("black", "grey"))
    window.FindElement(letra[0]).Update(disabled=True)


def desbloquear_atril(letra):
    """Desbloquea la letra enviada del atril"""
    window.FindElement(letra[0]).Update(button_color=("black", "white"))
    window.FindElement(letra[0]).Update(disabled=False)


def intercambio():
    """Intercambia matrix, intercambia bloqueo y desbloqueo de atril, la nueva letra pasa a tener la posicion de la anterior en letras_usadas y intercambia tablero"""
    global matrix, event, letras_usadas, letra_act, event_ant
    if letra_act != " ":
        pos = letras_usadas.index(matrix[event[0]][event[1]])
        desbloquear_atril(matrix[event[0]][event[1]])
        bloquear_atril(letra_act)
        matrix[event[0]][event[1]] = letra_act
        letras_usadas[pos] = (letra_act)
        window.FindElement(event).Update(letra_act)
        letra_act = " "
        event_ant = event


# --------------------------------------------------------------------- #
# --------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
#                           Funciones Tableros Simples                   #
# ---------------------------------------------------------------------- #
def bloquear_casilla(event):
    """Bloquea la casilla mandada"""
    if event != " ":
        window.FindElement(event).Update(button_color=("black", "grey"))
        window.FindElement(event).Update(disabled=True)


def desbloquear_casilla(event):
    """Desbloquea la casilla mandada"""
    if event != " ":
        window.FindElement(event).Update(button_color=("black", "green4"))
        window.FindElement(event).Update(disabled=False)


def desbloquear_tablero():
    """Desbloquea_todo el tablero"""
    for x in range(15):
        for y in range(15):
            window.FindElement((x, y)).Update(disabled=False)
            window.FindElement((x, y)).Update(button_color=("black", "white"))


def bloquear_tablero_con_excepcion(event):
    """Bloquea_todo el tablero a excepcion de la posicion enviada, la cual modifica su color a verde"""
    for x in range(15):
        for y in range(15):
            if (x, y) != event:
                window.FindElement((x, y)).Update(disabled=True)
                window.FindElement((x, y)).Update(button_color=("black", "grey"))
    window.FindElement(event).Update(button_color=("black", "green4"))


def bloquear_tablero():
    for x in range(15):
        for y in range(15):
            window.FindElement((x, y)).Update(disabled=True)
            window.FindElement((x, y)).Update(button_color=("black", "grey"))


def limpiar_tablero():
    """Limpia el tablero de letras cargadas en este turno, y borra las letras usadas"""
    for x in range(15):
        for y in range(15):
            if matrix[x][y] in letras_usadas:
                window.FindElement((x, y)).Update(" ")
    for a in range(len(letras_usadas)):
        desbloquear_atril(letras_usadas[a])
    for a in range(len(letras_usadas)):
        letras_usadas.remove(letras_usadas[0])


# --------------------------------------------------------------------- #
# --------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
#                           Funciones Tableros Complejas                 #
# ---------------------------------------------------------------------- #

def desbloquear_adyacentes(event):
    """Desbloquea las casillas adyacentes a la posicion enviada, para que el usuario elija una orientacion"""
    if event[1] < 14:
        window.FindElement((event[0], event[1] + 1)).Update(disabled=False)
        window.FindElement((event[0], event[1] + 1)).Update(button_color=("black", "green4"))
    if event[0] < 14:
        window.FindElement((event[0] + 1, event[1])).Update(disabled=False)
        window.FindElement((event[0] + 1, event[1])).Update(button_color=("black", "green4"))
    if event[0] > 0:
        window.FindElement((event[0] - 1, event[1])).Update(disabled=False)
        window.FindElement((event[0] - 1, event[1])).Update(button_color=("black", "green4"))


def bloqueo_desbloqueo_orientacion(event, event_ant, orientacion):
    """Bloquea y Desbloquea los casilleros, segun la orientacion que se elija"""
    if event[0] == event_ant[0] - 1:
        if event_ant[1] < 14:
            bloquear_casilla((event_ant[0], event_ant[1] + 1))
        if event_ant[0] < 14:
            bloquear_casilla((event_ant[0] + 1, event_ant[1]))
        if event[0] > 0:
            desbloquear_casilla((event[0] - 1, event[1]))
        orientacion = "vertical_arriba"

    if event[0] == event_ant[0] + 1:
        if event_ant[0] > 0:
            bloquear_casilla((event_ant[0] - 1, event_ant[1]))
        if event_ant[1] < 14:
            bloquear_casilla((event_ant[0], event_ant[1] + 1))
        if event[0] < 14:
            desbloquear_casilla((event[0] + 1, event[1]))
        orientacion = "vertical_abajo"

    if event[1] == event_ant[1] + 1:
        if event_ant[0] > 0:
            bloquear_casilla((event_ant[0] - 1, event_ant[1]))
        if event_ant[0] < 14:
            bloquear_casilla((event_ant[0] + 1, event_ant[1]))
        if event[1] < 14:
            desbloquear_casilla((event[0], event[1] + 1))
        orientacion = "horizontal"

    return orientacion


# ---------------------------------------------------------------------- #
# ---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
#                           Funciones Ayudantes                          #
# ---------------------------------------------------------------------- #
def is_empty(data_structure):
    """Retorna True si la estructura esta vacia, o False en caso contrario"""
    if data_structure:
        return False
    else:
        return True


def Inicio():
    """Esta funcion es la que hace borron y cuenta nueva, limpia todos los datos del turno, para que el usuario lo empiece de nuevo"""
    global event_ant, letras_usadas, letra_act, segunda_letra, primera_letra
    limpiar_tablero()
    reinicio_matrix()
    desbloquear_tablero()
    letra_act = " "
    letras_usadas = []
    event_ant = None
    segunda_letra = False
    primera_letra = True


def Cargar_primera_letra():
    global letra_act, event_ant, segunda_letra, primera_letra
    window.FindElement(event).Update(letra_act)  # pone letra en boton
    matrix[event[0]][event[1]] = letra_act  # guarda en que poscion esta esa letra
    bloquear_tablero_con_excepcion(event)
    desbloquear_adyacentes(event)  # desbloqueo los adyacentes para elegir orientacion con la segunda letra
    letras_usadas.append(letra_act)  # nueva letra usada
    bloquear_atril(letra_act)
    event_ant = event
    letra_act = " "
    segunda_letra = True  # seguro que la proxima letra es la segunda
    primera_letra = False


def Cargar_segunda_letra():
    global event_ant, letra_act, segunda_letra, orientacion
    print("Ingreso a bloqueo_desbloqueo")
    orientacion = bloqueo_desbloqueo_orientacion(event, event_ant,orientacion)  # compara posicion de primera letra con segunda, asi se sabe orientacion
    print("salgo de bloqueo_desbloqueo")
    matrix[event[0]][event[1]] = letra_act  # guarda en que poscion esta esa letra
    window.FindElement(event).Update(letra_act)  # pone letra en boton
    letras_usadas.append(letra_act)  # nueva letra usada
    bloquear_atril(letra_act)
    event_ant = event
    letra_act = " "
    segunda_letra = False  # ya se agrego la segunda letra


def Cargar_letra():  # a partir de la 2da letra, ya se la orientacion, por lo q se me ahce mas facil avanzar y agregar letras sin problemas
    global letra_act, event_ant
    matrix[event[0]][event[1]] = letra_act
    window.FindElement(event).Update(letra_act)
    if orientacion == "vertical_arriba":
        if event[0] > 0:
            desbloquear_casilla((event[0] - 1, event[1]))
    elif orientacion == "vertical_abajo":
        if event[0] < 14:
            desbloquear_casilla((event[0] + 1, event[1]))
    elif orientacion == "horizontal":
        if event[1] < 14:
            desbloquear_casilla((event[0], event[1] + 1))
    letras_usadas.append(letra_act)
    bloquear_atril(letra_act)
    event_ant = event
    letra_act = " "


# ---------------------------------------------------------------------- #
# ---------------------------------------------------------------------- #


window = sg.Window("ScrabbleAR").Layout(ventana_juego)

while True:
    event, values = window.read()
    # --- Cierre de Pestaña --- #
    if (event == None):
        break

        # --- Cuando es la primera letra del turno --- #
    if event[0] in diccionario and primera_letra:
        letra_act = event[0]
        desbloquear_tablero()

    # --- Si toco una letra y no es la primera del turno --- #
    if event[0] in diccionario and primera_letra == False:
        letra_act = event[0]

    # --- Si toco un Casillero  --- #
    if (event in boton):
        if matrix[event[0]][event[1]] in letras_usadas:  # si en este turno ya pusieron una letra en el casillero

            # --- Si elegí una letra antes de tocar el casillero --- #
            if letra_act != " ":
                intercambio()

            # -- Si No elegí una letra antes de tocar el casillero ---#
            else:
                # si es la primera letra de la palabra -> (se reinicia el turno)
                if matrix[event[0]][event[1]] == letras_usadas[0]:
                    Inicio()

                # si es la segunda letra de la palabra -> (se vuelve a elegir orientacion)
                else:
                    if matrix[event[0]][event[1]] == letras_usadas[1]:

                        if orientacion == "horizontal":
                            for a in range(len(letras_usadas)):
                                bloquear_casilla((event[0], event[1] + a))
                                matrix[event[0]][event[1]] = None
                                if letras_usadas[a] != letras_usadas[0]:
                                    desbloquear_atril(letras_usadas[a])
                                window.FindElement((event[0], event[1] + a)).Update(" ")

                            desbloquear_adyacentes((event[0], event[1] - 1))
                            event_ant=  (event[0], event[1] - 1)
                            segunda_letra = True
                            print("volvemos a elegir orientacion")

                        else:
                            if orientacion == "vertical_arriba":
                                print("vertical arriba")
                            else:
                                if orientacion == "vertical_abajo":
                                    print("vertical abajo")
                    # si es tercera o + ->(solo se borra, se habilita el atril, se actualiza letras_usadas y matrix)
                    else:
                        letras_usadas.remove(matrix[event[0]][event[1]])
                        desbloquear_atril(matrix[event[0]][event[1]])
                        window.FindElement(event).Update(letra_act)
                        bloquear_casilla((event[0],event[1]+1))
                        matrix[event[0]][event[1]] = None
                        event_ant = event

        else:
            # --- Si no se ingreso ninguna letra al tablero aún y la letra ya se eligió ---#
            if event_ant is None and letra_act != " ":
                print("cargar primera letra")
                Cargar_primera_letra()
            else:
                # si es la segunda letra que se ingresa al tablero y la letra ya se eligió
                if segunda_letra and letra_act != " ":
                    print("cargar segunda letra")
                    Cargar_segunda_letra()
                else:
                    # si se eligió letra y la orientacion ya fue marcada con las dos primeras letras
                    if letra_act != " ":
                        print("cargar tercera letra")
                        Cargar_letra()
