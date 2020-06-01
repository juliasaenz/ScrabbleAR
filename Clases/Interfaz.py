import PySimpleGUI as sg

class Interfaz:
    bt = {'size': (2, 1), 'font': ('Franklin Gothic Book', 10), 'button_color': ("black", "#F8F8F8")}
    def __init__(self,matriz,jugador):
        _tutorial = []
        _tablero = []
        self._jugador = jugador
        self._matriz = []
        self._matriz = matriz
        self._tam = 15

    def crear_matriz(self,matriz):
        clave = 0
        for z in range(self._tam):
            matriz.append([])
            for x in range(self._tam):
                prueba = (clave,z,x)
                print(prueba)
                matriz[z].append(sg.Button(self._matriz._matriz[z][x].devolver_estado(), **self.bt, key= prueba))
                #matriz[z].append(sg.Button("", **self.bt, key=clave))
                clave = clave + 1

    def crear_letras(self,tablero):
        b = lambda n: sg.Button(n, **self.bt)
        tablero.append([])
        #tablero[-1].append(sg.Frame(layout=[[b("A"), b("C"), b("S"), b("M")]], title="Letras Disponibles"))
        botones = []
        for ficha in self._jugador.get_atril():
            botones.append(b(ficha))
        tablero[-1].append(sg.Frame(layout=[botones], title="Letras Disponibles"))
        tablero[-1].append(sg.Ok("Terminar Turno"))

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

    def crear_configuracion(self):
        ''' Configuración'''

    def mostrar_interfaz(self):
        palabra = ""
        letra_act = ""
        boton = list(range(15 * 15))
        # ejecución
        tutorial = self.crear_tutorial()
        window = sg.Window("01-06-mio").Layout(tutorial)
        event, values = window.read()
        if event == None:
            window.close()
        if event == "Jugar":
            window.close()
            sg.theme("DarkTeal4")
            tablero = self.dibujar_tablero()
            window = sg.Window("01-06-mio").Layout(tablero)
            while True:
                event, values = window.read()
                print(event)
                self._jugador.sacar_ficha(letra_act)
                print(self._jugador.imprimir_atril())
                if (event == None):
                    break
                if (event[0] in boton):
                    window.FindElement(event).Update(letra_act)
                    self._matriz._matriz[event[1]][event[2]].ocupar_casillero(letra_act)
                    if(letra_act != ""):
                        palabra = palabra + letra_act
                    letra_act = ""
                else:
                    letra_act = event
                if(event == "Terminar Turno"):
                    print("yay")