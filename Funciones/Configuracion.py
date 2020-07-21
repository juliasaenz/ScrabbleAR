import PySimpleGUI as sg
import estilo


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
