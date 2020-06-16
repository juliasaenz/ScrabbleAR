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
                [sg.Text("Presiona Jugar para ir a la interfaz el juego:"), sg.Button("Ok")]
                ]
    tutorial = [[sg.Frame(layout=interfaz, title="Tutorial")]]
    return tutorial

def inicio():
    '''El inicio'''
    interfaz = [[sg.InputText("Tu nombre")],
                [sg.Listbox(values=(('Nivel 1',"Nivel 2","Nivel 3")), size=(30, 3))],
                [sg.Button("Jugar")]
                ]
    inicio = [[sg.Frame(layout=interfaz,title="Inicio")]]
    return inicio