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

jugador = Jugador("Felipe", bolsa)
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
pos_usadas = []
segunda_letra = False
primera_letra = True
tercera_o_mas = False
letra_act = " "
boton = crear_boton()
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
    window.FindElement(letra).Update(button_color=("black", "grey"))
    window.FindElement(letra).Update(disabled=True)


def desbloquear_atril(letra):
    """Desbloquea la letra enviada del atril"""
    window.FindElement(letra).Update(button_color=("black", "white"))
    window.FindElement(letra).Update(disabled=False)


def intercambio():
    """Intercambia matrix, intercambia bloqueo y desbloqueo de atril, la nueva letra pasa a tener la posicion de la anterior en letras_usadas y intercambia tablero"""
    global event, letras_usadas, letra_act, pos_usadas, matrix
    i = 0
    for i in range(len(pos_usadas)):
        if event == pos_usadas[i]:
            numero = i
    desbloquear_atril(letras_usadas[numero])
    letras_usadas[numero] = letra_act
    bloquear_atril(letra_act)
    window.FindElement(event).Update(letra_act[0])
    letra_act = " "


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
    for a in range(len(pos_usadas)):
        window.FindElement(pos_usadas[a]).Update(" ")


def insertar_casilla(aux):
    """Inserta en el evento(casilla) la letra enviada"""
    window.FindElement(event).Update(aux[0])


def act_orientacion():
    """Indica la orientacion de la palabra que se esta formando segun la pos de 1° y 2° letras"""
    global orientacion, pos_usadas, event
    if event < pos_usadas[0]:
        orientacion = "vertical_arriba"
    if (event[0], event[1] - 1) == pos_usadas[0]:
        orientacion = "horizontal"
    if (event[0] - 1, event[1]) == pos_usadas[0]:
        orientacion = "vertical_abajo"


def bloqueo_orientacion():
    """Bloquea las casillas adyacentes segun la orientacion"""
    global pos_usadas, orientacion
    if orientacion == "vertical_arriba":
        if pos_usadas[0][1] + 1 < 14:
            bloquear_casilla((pos_usadas[0][0], pos_usadas[0][1] + 1))
        if pos_usadas[0][0] + 1 < 14:
            bloquear_casilla((pos_usadas[0][0] + 1, pos_usadas[0][1]))
    if orientacion == "vertical_abajo":
        if pos_usadas[0][1] + 1 < 14:
            bloquear_casilla((pos_usadas[0][0], pos_usadas[0][1] + 1))
        if pos_usadas[0][0] > 0:
            bloquear_casilla((pos_usadas[0][0] - 1, pos_usadas[0][1]))
    if orientacion == "horizontal":
        if pos_usadas[0][0] > 0:
            bloquear_casilla((pos_usadas[0][0] - 1, pos_usadas[0][1]))
        if pos_usadas[0][0] < 14:
            bloquear_casilla((pos_usadas[0][0] + 1, pos_usadas[0][1]))


def desbloqueo_siguiente_orientacion():
    """Desbloquea la siguiente casilla según la orientación del evento actual"""
    global event, orientacion
    if orientacion == "vertical_arriba":
        if event[0] > 0:
            desbloquear_casilla((event[0] - 1, event[1]))
    if orientacion == "vertical_abajo":
        if event[0] < 14:
            desbloquear_casilla((event[0] + 1, event[1]))
    if orientacion == "horizontal":
        if event[1] < 14:
            desbloquear_casilla((event[0], event[1] + 1))


# --------------------------------------------------------------------- #
# --------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
#                           Funciones Tableros Complejas                 #
# ---------------------------------------------------------------------- #

def desbloquear_adyacentes(event):
    """Desbloquea las casillas adyacentes a la posicion enviada, para que el usuario elija una orientacion"""
    if event[0] > 0:
        desbloquear_casilla((event[0] - 1, event[1]))
    if event[0] < 14:
        desbloquear_casilla((event[0] + 1, event[1]))
    if event[1] < 14:
        desbloquear_casilla((event[0], event[1] + 1))


def bloqueo_desbloqueo_orientacion():
    """Bloquea y Desbloquea los casilleros, segun la orientacion que se elija"""
    act_orientacion()
    bloqueo_orientacion()
    desbloqueo_siguiente_orientacion()


def volver_atras_orientacion():
    """Vuelve atras los casilleros cargados, a excepcion del primero, para elegir orientacion"""
    global pos_usadas, letras_usadas, segunda_letra, tercera_o_mas
    aux = len(pos_usadas)
    if orientacion == "horizontal":
        # --- primero bloquea la casilla libre --- #
        if pos_usadas[aux - 1][1] < 14:
            bloquear_casilla((pos_usadas[aux - 1][0], pos_usadas[aux - 1][1] + 1))
    if orientacion == "vertical_arriba":
        if pos_usadas[aux - 1][0] - 1 > 0:
            bloquear_casilla((pos_usadas[aux - 1][0] - 1, pos_usadas[aux - 1][1]))
    if orientacion == "vertical_abajo":
        if pos_usadas[aux - 1][0] + 1 < 14:
            bloquear_casilla((pos_usadas[aux - 1][0] + 1, pos_usadas[aux - 1][1]))
    # --- bloquea desde la ultima casilla usada, hasta la primera --- #
    for a in range(aux - 1, 0, -1):
        bloquear_casilla(pos_usadas[a])
        window.FindElement(pos_usadas[a]).Update(" ")
        desbloquear_atril(letras_usadas[a])

    # --- Se desbloquean adyacentes, se vuelve a inicializar letras y pos usadas a excepcion de la primera que se queda --- #
    desbloquear_adyacentes(pos_usadas[0])
    cambio = letras_usadas[0]
    letras_usadas = []
    letras_usadas.append(cambio)
    cambio = pos_usadas[0]
    pos_usadas = []
    pos_usadas.append(cambio)
    segunda_letra = True
    tercera_o_mas = False


def regresar_casillero(numero):
    """Regresa los casilleros"""
    global pos_usadas, letras_usadas, orientacion
    # si tiene una casilla disponible, la bloquea
    if len(pos_usadas) <= 6:
        if orientacion == "horizontal":
            bloquear_casilla((pos_usadas[len(pos_usadas) - 1][0], pos_usadas[len(pos_usadas) - 1][1] + 1))
        if orientacion == "vertical_abajo":
            bloquear_casilla((pos_usadas[len(pos_usadas) - 1][0] + 1, pos_usadas[len(pos_usadas) - 1][1]))
        if orientacion == "vertical_arriba":
            bloquear_casilla((pos_usadas[len(pos_usadas) - 1][0] - 1, pos_usadas[len(pos_usadas) - 1][1]))

    # recorre y bloquea todas las casillas hasta la marcada
    for aux in range(len(pos_usadas), numero, -1):
        bloquear_casilla(pos_usadas[aux - 1])
        window.FindElement(pos_usadas[aux - 1]).Update(" ")
        desbloquear_atril(letras_usadas[aux - 1])
        pos_usadas.remove(pos_usadas[aux - 1])
        letras_usadas.remove(letras_usadas[aux - 1])

    # habilita la proxima casilla
    if orientacion == "horizontal":
        desbloquear_casilla((pos_usadas[len(pos_usadas) - 1][0], pos_usadas[len(pos_usadas) - 1][1] + 1))
    if orientacion == "vertical_abajo":
        desbloquear_casilla((pos_usadas[len(pos_usadas) - 1][0] + 1, pos_usadas[len(pos_usadas) - 1][1]))
    if orientacion == "vertical_arriba":
        desbloquear_casilla((pos_usadas[len(pos_usadas) - 1][0] - 1, pos_usadas[len(pos_usadas) - 1][1]))


def analizar_evento():
    """compara al evento con la posicion de las letras usadas, para saber cuales  tiene que quitar"""
    global event, pos_usadas
    if event == pos_usadas[2]:
        regresar_casillero(2)
    else:
        if event == pos_usadas[3]:
            regresar_casillero(3)
        else:
            if event == pos_usadas[4]:
                regresar_casillero(4)
            else:
                if event == pos_usadas[5]:
                    regresar_casillero(5)
                else:
                    if event == pos_usadas[6]:
                        regresar_casillero(6)


# ---------------------------------------------------------------------- #
# ---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
#                           Funciones Ayudantes                          #
# ---------------------------------------------------------------------- #
def Inicio():
    """Esta funcion es la que hace borron y cuenta nueva, limpia todos los datos del turno, para que el usuario lo empiece de nuevo"""
    global letras_usadas, letra_act, segunda_letra, primera_letra, pos_usadas, tercera_o_mas
    limpiar_tablero()
    desbloquear_tablero()
    pos_usadas = []
    letra_act = " "
    letras_usadas = []
    segunda_letra = False
    primera_letra = True
    tercera_o_mas = False

def Cargar_primera_letra():
    """Carga la primera letra en tabla, """
    global letra_act, segunda_letra, primera_letra, pos_usadas
    pos_usadas.append(event)
    letras_usadas.append(letra_act)
    insertar_casilla(letra_act)
    bloquear_atril(letra_act)
    bloquear_tablero_con_excepcion(event)
    desbloquear_adyacentes(event)
    primera_letra = False
    segunda_letra = True
    letra_act = " "

def Cargar_segunda_letra():
    global letra_act, segunda_letra, pos_usadas, tercera_o_mas
    pos_usadas.append(event)
    letras_usadas.append(letra_act)
    insertar_casilla(letra_act)
    bloquear_atril(letra_act)
    bloqueo_desbloqueo_orientacion()
    letra_act = " "
    segunda_letra = False
    tercera_o_mas = True

def Cargar_adicional_letra():
    global letra_act, event, pos_usadas
    pos_usadas.append(event)
    letras_usadas.append(letra_act)
    insertar_casilla(letra_act)
    bloquear_atril(letra_act)
    if len(pos_usadas) < 7:  # si es la letra N° 7 no tiene xq agregar una siguiente casilla
        desbloqueo_siguiente_orientacion()
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
        letra_act = event
        desbloquear_tablero()

    # --- Si toco una letra y no es la primera del turno --- #
    if event[0] in diccionario and primera_letra == False:
        letra_act = event

    # --- Si toco tablero sin elegir letra --- #
    if event in boton and letra_act == " ":
        if event == pos_usadas[0]:  # si el evento es la 1° letra puesta
            Inicio()
        else:
            if event == pos_usadas[1]:  # si es la 2°
                volver_atras_orientacion()
            else:
                analizar_evento()  # si es la 3° o +
    if event in boton and event in pos_usadas:
        intercambio()
    else:
        # --- Si toco tablero habiendo elegido la primera letra para poner --- #
        if event in boton and letra_act != " " and primera_letra:
            Cargar_primera_letra()
        else:
            # --- Si toco tablero habiendo elegido la 2°  letra --- #
            if event in boton and letra_act != " " and segunda_letra:
                Cargar_segunda_letra()
            else:
                # --- Si toco tablero eligiendo 3° o mas --- #
                if event in boton and tercera_o_mas and letra_act != " ":
                    Cargar_adicional_letra()
