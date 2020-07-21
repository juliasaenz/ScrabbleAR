import PySimpleGUI as sg
import estilo


def tutorial():
    """ El tutorial """
    tutorial = []
    sg.theme("DarkBlack")
    interfaz = [[sg.Text("Bienvenido")],
                [sg.Text("Para poder conseguir puntos, tienes que armar palabras,")],
                [sg.Text("estas se pueden armar tanto vertical, como horizontal.")],
                [sg.Text("el puntaje de cada palabra se debe a dos factores:")],
                [sg.Text("1-El puntaje individual de cada letra")],
                [sg.Text("2-Los efectos de cada casilla ")],
                [sg.Text("Presiona Jugar para ir a la interfaz el juego:"), sg.Button("Ok",**estilo.tt)]
                ]
    tutorial = [[sg.Frame(layout=interfaz, title="Tutorial", **estilo.tt)]]
    return tutorial


def inicio():
    """El inicio"""
    interfaz = [[sg.InputText("Tu nombre",**estilo.tt)],
                [sg.Listbox(values=('fácil', "medio", "difícil"), size=(30, 3), **estilo.tt)],
                [sg.Button("Nueva Partida",**estilo.tt), sg.Button("Continuar",**estilo.tt)]
                ]
    inicio = [[sg.Frame(layout=interfaz, title="Inicio", **estilo.bt)]]
    return inicio
