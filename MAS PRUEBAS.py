from importaciones import *

#____________________INICIO_____________________________#

# armo el diccionario de palabras válidas
diccionario = palabras_sin_tilde()

# abro el json del nivel que quiera
nivel = open("Archivos/nivel1", "r")
config = json.load(nivel)

# armo la bolsa de letras (es una lista)
bolsa = []
for letra in config["cantidad"].keys():
    for veces in range(config["cantidad"][letra]):
        bolsa.append(letra)

#abro el tutorial
tutorial = tutorial()
window = sg.Window("Reacomodar todo...").Layout(tutorial)
event, values = window.read()

jugador = Jugador("Julia",bolsa)

#paso a juego
if event == None:
    window.close()
if event == "Ok":
    window.close()
    tabla = Tablero()
    boton = tabla.referencia_a_botones()

# ____________________JUEGO_____________________________#
    #Ventana Juego
    ventana_juego = [[sg.Frame(layout=tabla.dibujar(), title="Tablero")],
                     [],
                     [sg.Frame(layout=jugador.dibujar(),key=jugador.get_nombre(), title="Atril de "+jugador.get_nombre()),sg.Ok("Terminar Turno")]
                     ]

    window = sg.Window("ScrabbleAR").Layout(ventana_juego)
    #Mientras Juego:

    #aca guardo letra actual, las pos de los casilleros, etc
    turno = Turno(jugador.get_atril())

    while True:
        event, values = window.read()
        print("event: ",event)
        print("letra actual: ",turno.get_letra_actual())
        # que boton toque?
        if (event == None):
            break
        if (event in boton):
            #estructura
            if(not tabla.casillero_ocupado(event)):
                try:
                    #ocupa en la matriz tablero
                    tabla.ocupar_casillero(turno.get_letra_actual(),event)
                    #saca del atril
                    jugador.sacar_ficha(turno.get_letra_actual())
                    #agrega a usados
                    turno.agregar_casillero(event)
                    #esto actualiza la ventana
                    window.FindElement(event).Update(turno.get_letra_actual())
                except(ValueError):
                    print("ESA YA LA USASTE!")
            else:
                #desocupa en la matriz tablero
                letra_vieja = tabla.vaciar_casillero(event)
                #agrega al atril
                jugador.agregar_ficha(turno.get_letra_actual())
                #saca de usados
                turno.sacar_casillero(event)
                #esto actualiza la ventana
                window.FindElement(letra_vieja).Update(disabled = False)
                window.FindElement(event).Update(turno.get_letra_actual())
            #actualiza la letra actual
            turno.set_letra_actual("")
        else:
            turno.set_letra_actual(event[0])
            window.FindElement(event).Update(disabled = True)
            print(jugador.get_atril())
        if (event == "Terminar Turno"):
            #reponer el atril del jugador
            jugador.reponer_atril(bolsa)
            # actualizar atril
            i = 0
            for dato in jugador.get_atril():
                #ARREGLAR no se actualizan las keys
                window.FindElement(turno.get_atril()[i]).Update(dato, disabled=False)
                i = i + 1
            #fin de turno
            print(turno.get_palabra(), " es valida?: ",
                  palabra_es_valida(turno.get_palabra, diccionario, config["tipos"]))
            if(palabra_es_valida(turno.get_palabra, diccionario, config["tipos"])):
                turno.fin_turno(tabla.get_matriz(),config["puntos"],"h")

            #PROVISORIO: Esto esta aca para poder probar turnos consecutivos nomas
            window.FindElement("Terminar Turno").Update(disabled=False)