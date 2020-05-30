import PySimpleGUI as sg

def tutorial():
    ''' El tutorial '''
    tutorial = []
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
