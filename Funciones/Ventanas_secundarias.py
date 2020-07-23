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
                [sg.Listbox(values=('fácil', "medio", "difícil", "customizar"), size=(30, 4), **estilo.tt)],
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


def configurar_letras(dicc):
    l = []
    inp = []

    for letra in dicc.keys():
        l.append(sg.Text(" " + letra.upper(), **estilo.bt))
        inp.append(sg.Input(size=(2, 1), pad=(6, 3), default_text=(dicc[letra])))

    extra_layout = [l, inp, [sg.Ok("Listo"), sg.Cancel("Cancelar")]]

    extra_window = sg.Window("Configuración Extra", extra_layout, **estilo.tt)
    while True:
        event4, values4 = extra_window.Read()
        if event4 == sg.WIN_CLOSED or event4 == "Cancelar":
            extra_window.Close()
            break
        if event4 == "Listo":
            try:
                values4 = {int(k): int(v) for k, v in values4.items()}
                if sum(values4.values()) == 0:
                    sg.Popup("Todas las letras no pueden ser 0")
                else:
                    i = 0
                    for clave in dicc.keys():
                        dicc[clave] = values4[i]
                        i = i + 1
                    extra_window.Close()
                    break
            except ValueError:
                sg.Popup("Por favo solo ingrese números")


def configurar_dificultad(config, niveles, bolsa, tiempo):
    lista = ['', "fácil", "medio", "difícil"]

    configurar = [[sg.Text("Dificultad Computadora: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)],
                  [sg.Text("Cantidad fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None),
                   sg.Button("Configurar "
                             "individualmente", key="config_1", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Puntaje fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None),
                   sg.Button("Configurar "
                             "individualmente", key="config_2", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Tablero: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)],
                  [sg.Text("Tiempo: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)]
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
            break
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
                if len(values2[5]) > 0:
                    t = (niveles["tiempo"][values2[5]]*100 - (config["tiempo"]*100 - tiempo))
                    config["tiempo"] = niveles["tiempo"][values2[5]]
                    return t
                c_window.Close()
                break
            except KeyError:
                print("El error tiene que estar por aca: ", values2)
            c_window.Close()
        elif event2 == "config_1":
            c_window.Hide()
            configurar_letras(config["cantidad"])

            # bolsa
            bolsa.clear()
            for letra in config["cantidad"].keys():
                for veces in range(config["cantidad"][letra]):
                    bolsa.append(letra)

            c_window.UnHide()
        elif event2 == "config_2":
            c_window.Hide()
            configurar_letras(config["puntos"])
            c_window.UnHide()


def ventana_shuffle(atril):
    lista = []
    i = 0
    for letra in atril:
        lista.append(sg.Button(letra, key=str(i), **estilo.bt, button_color=("black", "white")))
        i = i + 1

    v_layout = [
        [sg.Text("Elija qué fichas cambiar", **estilo.tt)], lista, [],
        [sg.Ok(**estilo.tt), sg.Button("Limpiar", **estilo.tt),
         sg.Cancel("Cancelar", **estilo.tt)]
    ]
    v_window = sg.Window("Da Shuffle", v_layout, **estilo.tt)

    fichas_a_cambiar = []

    while True:
        event3, values3 = v_window.Read()
        if event3 == sg.WIN_CLOSED or event3 == "Cancelar":
            v_window.Close()
            return []
            break
        elif event3 == "Limpiar":
            for i in range(7):
                v_window.FindElement(str(i)).Update(disabled=False)
            fichas_a_cambiar.clear()
        elif event3 in "0123456":
            v_window.FindElement(event3).Update(disabled=True)
            fichas_a_cambiar.append(event3)
        elif event3 == "Ok":
            return fichas_a_cambiar
            break
