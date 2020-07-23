import PySimpleGUI as sg
import estilo


def tutorial():
    """ El tutorial """
    sg.theme("DarkBlack")
    interfaz = [[sg.Text("Bienvenido")],
                [sg.Text("Para poder conseguir puntos, tienes que armar palabras,")],
                [sg.Text("estas se pueden armar tanto vertical, como horizontal.")],
                [sg.Text("el puntaje de cada palabra se debe a dos factores:")],
                [sg.Text("1-El puntaje individual de cada letra")],
                [sg.Text("2-Los efectos de cada casilla ")],
                [sg.Text("Presiona Jugar para ir a la interfaz el juego:"), sg.Button("Ok", **estilo.tt)]
                ]
    tutorial = [[sg.Frame(layout=interfaz, title="Tutorial", **estilo.tt)]]
    return tutorial


def inicio():
    """El inicio"""
    interfaz = [[sg.InputText("Tu nombre", **estilo.tt)],
                [sg.Listbox(values=('fácil', "medio", "difícil"), size=(30, 3), **estilo.tt)],
                [sg.Button("Nueva Partida", **estilo.tt), sg.Button("Continuar", **estilo.tt)]
                ]
    inicio = [[sg.Frame(layout=interfaz, title="Inicio", **estilo.bt)]]
    return inicio


# Funciones para niveles
def actualizar_todo_dicc(config, niveles, dificultad):
    config["puntos"] = niveles["puntos"][dificultad][dificultad]
    config["cantidad"] = niveles["letras"][dificultad][dificultad]
    config["palabras"] = niveles["palabras"][dificultad]
    config["tipos"] = niveles["tipos"][dificultad]
    config["compu"] = niveles["compu"][dificultad]


def configurar_dificultad(config, niveles):
    lista = ['', "fácil", "medio", "difícil"]

    configurar = [[sg.Text("Dificultad Computadora: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)],
                  [sg.Text("Puntaje fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None),
                   sg.Button("Configurar "
                             "individualmente", key="config_1", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Cantidad fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None),
                   sg.Button("Configurar "
                             "individualmente", key="config_2", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Tablero: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)]
                  ]

    c_layout = [
        [sg.Text("Seleccionar nivel: ", **estilo.tt),
         sg.Combo(['', "fácil", "medio", "difícil"], **estilo.tt, default_value=None)],
        [sg.Frame(layout=configurar, title="Configuración manual")],
        [sg.Ok("Confirmar cambios", **estilo.tt, button_color=("#FAFAFA", "#151514")),
         sg.Cancel("Cancelar", **estilo.tt, button_color=("#FAFAFA", "#151514"))]
    ]

    c_window = sg.Window("Configuración", c_layout, **estilo.tt)
    while True:
        event2, values2 = c_window.Read()
        print("event2: ", event2, " values2: ", values2)
        if event2 == sg.WIN_CLOSED or event2 == "Cancelar":
            c_window.Close()
        elif event2 == "Confirmar cambios":
            try:
                if len(values2[0]) > 0:
                    actualizar_todo_dicc(config, niveles, values2[0])
                if len(values2[1]) > 0:
                    config["compu"] = niveles["compu"][values2[1]]
                if len(values2[2]) > 0:
                    config["puntos"] = niveles["compu"][values2[2]]
                if len(values2[3]) > 0:
                    config["cantidad"] = niveles["letras"][values2[3]]
            except KeyError:
                print("El error tiene que estar por aca: ", values2)
            c_window.Close()
        elif event2 == "config_1":
            sg.popup("HELLO")
        elif event2 == "config_2":
            sg.popup("config")

        break

    def ventana_shuffle():
        v_layout: [
            sg.Text("shuflle shuffle yay")
        ]
        v_window = sg.Window("Da Shuffle", v_layout, **estilo.tt)
        while True:
            event3, values3 = v_window.Read()
            if event3 == sg.WIN_CLOSED or event3 == "Cancelar":
                c_window.Close()
