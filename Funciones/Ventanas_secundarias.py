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
def actualizar_todo_dicc(config, niveles, dificultad, tiempo, bolsa, act_config):
    config["puntos"] = niveles["puntos"][dificultad][dificultad]
    config["cantidad"] = niveles["letras"][dificultad][dificultad]
    config["palabras"] = niveles["palabras"][dificultad]
    config["tipos"] = niveles["tipos"][dificultad]
    config["compu"] = niveles["compu"][dificultad]

    # bolsa
    bolsa.clear()
    for letra in config["cantidad"].keys():
        for veces in range(config["cantidad"][letra]):
            bolsa.append(letra)

    if tiempo in config.keys():
        t = (niveles["tiempo"][dificultad] * 100 - (config["tiempo"] * 100 - tiempo))
        config["tiempo"] = niveles["tiempo"][dificultad]
        return t
    else:
        config["tiempo"] = niveles["tiempo"][dificultad]

    act_config.clear()
    for i in range(7):
        act_config.append(dificultad)


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


def configurar_dificultad(config, niveles, bolsa, tiempo, act_config):
    lista = ['', "fácil", "medio", "difícil"]

    configurar = [[sg.Text("Dificultad Computadora: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)],
                  [sg.Text("Cantidad fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None),
                   sg.Button("Configurar "
                             "individualmente", key="config_1", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Puntaje fichas: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None),
                   sg.Button("Configurar "
                             "individualmente", key="config_2", **estilo.tt, button_color=("#FAFAFA", "#151514"))],
                  [sg.Text("Tablero: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)],
                  [sg.Text("Tiempo: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)],
                  [sg.Text("Tipos de palabras: ", **estilo.tt), sg.Combo(lista, **estilo.tt, default_value=None)]
                  ]

    c_layout = [
        [sg.Text("Seleccionar nivel: ", **estilo.tt),
         sg.Combo(['', "fácil", "medio", "difícil"], **estilo.tt, default_value=None)],
        [sg.Frame(layout=configurar, title="Configuración manual")],
        [sg.Ok("Confirmar cambios", **estilo.tt, button_color=("#FAFAFA", "#151514")),
         sg.Cancel("Cancelar", **estilo.tt, button_color=("#FAFAFA", "#151514")),
         sg.Button("Configuración actual", **estilo.tt, button_color=("#FAFAFA", "#151514"))]
    ]

    c_window = sg.Window("Configuración", c_layout, **estilo.tt)
    while True:
        event2, values2 = c_window.Read()
        print("event2: ", event2, " values2: ", values2)
        if event2 == sg.WIN_CLOSED or event2 == "Cancelar":
            c_window.Close()
            break
        elif event2 == "Configuración actual":
            print("act config: ", act_config)
            sg.Popup('''Configuración: \n
     Nivel: {0} \n
     Dificultad computadora: {1} \n
     Cantidad de fichas: {2} \n
     Puntaje de fichas: {3} \n
     Tablero: {4} \n
     Tiempo: {5} \n
     Tipos de palabras: {6} \n'''.format(act_config[0], act_config[1], act_config[2], act_config[3],
                                         act_config[4], act_config[5], act_config[6]))
        elif event2 == "Confirmar cambios":
            c_window.Close()
            if len(values2[0]) > 0:
                return actualizar_todo_dicc(config, niveles, values2[0], tiempo, bolsa, act_config)
            if len(values2[1]) > 0:
                config["compu"] = niveles["compu"][values2[1]]
                act_config[1] = values2[1]
            if len(values2[2]) > 0:
                config["cantidad"] = niveles["letras"][values2[2]][values2[2]]
                act_config[2] = values2[2]
                # bolsa
                bolsa.clear()
                for letra in config["cantidad"].keys():
                    for veces in range(config["cantidad"][letra]):
                        bolsa.append(letra)
            if len(values2[3]) > 0:
                config["puntos"] = niveles["puntos"][values2[3]][values2[3]]
                act_config[3] = values2[3]
            if len(values2[4]) > 0:
                config["tipos"] = niveles["tipos"][values2[4]]
                act_config[4] = values2[4]
            if len(values2[5]) > 0:
                if "tiempo" in config.keys():
                    t = (niveles["tiempo"][values2[5]] * 100 - (config["tiempo"] * 100 - tiempo))
                    config["tiempo"] = niveles["tiempo"][values2[5]]
                    print("a ver si es esto lo que me esta causando errores: ", niveles["tiempo"][values2[5]])
                    return t
                else:
                    config["tiempo"] = niveles["tiempo"][values2[5]]
                act_config[5] = values2[15]
            if len(values2[6]) > 0:
                config["palabras"] = niveles["palabras"][values2[6]]
                act_config[6] = values2[6]
            break
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
            v_window.Close()
            break
