import PySimpleGUI as sg

class Interfaz:
    bt = {'size': (2, 1), 'font': ('Franklin Gothic Book', 10), 'button_color': ("black", "#F8F8F8")}
    def __init__(self,matriz):
        _tutorial = []
        _tablero = []
        self._matriz = []
        self._matriz = matriz
        self._tam = 15

    def crear_matriz(self,matriz):
        clave = 0
        self._matriz.imprimir_tablero()
        for z in range(self._tam):
            matriz.append([])
            for x in range(self._tam):
                #matriz[z].append(sg.Button(self._matriz[z].devolver_estado(), **self.bt, key=clave))
                matriz[z].append(sg.Button(self._matriz._matriz[z][x].devolver_estado(), **self.bt, key=clave))
                #matriz[z].append(sg.Button("", **self.bt, key=clave))
                clave = clave + 1

    def crear_letras(self,tablero):
        b = lambda n: sg.Button(n, **self.bt)
        tablero.append([])
        tablero[-1].append(sg.Frame(layout=[[b("A"), b("C"), b("S"), b("M")]], title="Letras Disponibles"))

    def dibujar_tablero(self):
        matriz = []
        self.crear_matriz(matriz)
        tablero = [[sg.Frame(layout=matriz, title="Tablero")]]
        self.crear_letras(tablero)
        return tablero

    # funciones_creación_tutorial
    def crear_tutorial(self):
        sg.theme("DarkGreen4")
        interfaz = [[sg.Text("Bienvenido")],
                    [sg.Text("Para poder conseguir puntos, tienes que armar palabras,")],
                    [sg.Text("estas se pueden armar tanto vertical, como horizontal.")],
                    [sg.Text("el puntaje de cada palabra se debe a dos factores:")],
                    [sg.Text("1-El puntaje individual de cada letra")],
                    [sg.Text("2-Los efectos de cada casilla ")],
                    [sg.Text("Presiona Jugar para ir a la interfaz el juego:"), sg.Button("Jugar")]
                    ]
        tutorial = [[sg.Frame(layout=interfaz, title="Tutorial")]]
        return tutorial

    def mostrar_interfaz(self):
        letra_act = ""
        boton = list(range(15 * 15))
        # ejecución
        tutorial = self.crear_tutorial()
        window = sg.Window("ScrabbleAR").Layout(tutorial)
        event, values = window.read()
        if event == None:
            window.close()
        if event == "Jugar":
            window.close()
            sg.theme("DarkTeal4")
            tablero = self.dibujar_tablero()
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