import PySimpleGUI as sg

# predeterminado

bt = {'size': (2, 1), 'font': ('Franklin Gothic Book', 10), 'button_color': ("black", "#F8F8F8")}


#funciones_creacion_tablero:
def crear_matriz(matriz):
    clave = 0
    for z in range(15):
        matriz.append([])
        for x in range(15):
            matriz[z].append(sg.Button("", **bt, key=clave))
            clave=clave + 1

def crear_letras(tablero):
    b = lambda n: sg.Button(n, **bt)
    tablero.append([])
    tablero[-1].append(sg.Frame(layout=[[b("A"), b("C"), b("S"), b("M")]], title="Letras Disponibles"))

def dibujar_tablero():
    matriz=[]
    crear_matriz(matriz)
    tablero=[[sg.Frame(layout=matriz, title="Tablero")]]
    crear_letras(tablero)
    return tablero

#funciones_creación_tutorial
def crear_tutorial():
    sg.theme("DarkGreen4")
    interfaz=[[sg.Text("Bienvenido")],
              [sg.Text("Para poder conseguir puntos, tienes que armar palabras,")],
              [sg.Text("estas se pueden armar tanto vertical, como horizontal.")],
              [sg.Text("el puntaje de cada palabra se debe a dos factores:")],
              [sg.Text("1-El puntaje individual de cada letra")],
              [sg.Text("2-Los efectos de cada casilla ")],
              [sg.Text("Presiona Jugar para ir a la interfaz el juego:"), sg.Button("Jugar")]
              ]
    tutorial=[[sg.Frame(layout=interfaz, title="Tutorial")]]
    return tutorial

#variables
letra_act = ""
boton = list(range(15 * 15))
tutorial=[]
tablero=[]

#ejecución
tutorial=crear_tutorial()
window=sg.Window("ScrabbleAR").Layout(tutorial)

event, values=window.read()
if event==None:
    window.close()
if event=="Jugar":
    window.close()
    sg.theme("DarkTeal4")
    tablero=dibujar_tablero()
    window = sg.Window("ScrabbleAR").Layout(tablero)
    while True:
        event, values = window.read()
        if (event == None):
            break
        if (event in boton):
            window.FindElement(event).Update(letra_act)
            letra_act = ""
        else:
            letra_act = event
