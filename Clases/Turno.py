""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from Funciones.funciones_palabras import palabra_es_valida


class Turno:
    """
    VARIABLES DE INSTANCIA
    :str _letras: letras usadas en el turno (sin orden)
    :str _palabra: str: la palabra que se forma
    :set _casilleros_usados: guarda las posiciones de los casilleros usados
    :str _letra_actual: guarda el valor de la letra actual
    :str _pos_actual: el último valor del atril presionado
    :str _orientacion: la orientación de la palabra
    :bool _turno_usuario_: True si es el turno del usuario
    :str[] _lista_palabras: lista de palabras jugadas en el la partida
    :int _puntaje: los puntos de la palabra jugada en el punto
    :bool primer_turno: True hasta que se juege el primer turno

    MÉTODOS
    :get_primer_turno() → self._primer_turno
    :jugue_primer_turno(): pone self._primer_turno en False
    :validar_turno(): devuelve True si es el primer turno y la palabra ubicada tiene una letra en el casillero del
    medio, o si ya no es el primer turno → bool
    :set_letra_actual(str): actualiza self._letra_actual
    :get_letra_actual(): → self._letra_actual
    :set_pos_actual(tuple) → actualiza self._pos_actual
    :get_pos_actual() → self._pos_actual
    :agregar_casillero(tuple): agrega una posicion de casillero a self._casilleros_usados, si es el segundo elemento
    agregado atualiza la orientación
    :sacar_casillero(tuple): saca el casillero  pasado de self._casilleros_usados
    :get_casilleros_usados() → self._casilleros_usados
    :set_casilleros_usados(): actualiza self._casilleros_usados
    :definir_palabra(Tablero): ordena el arreglo de posiciones usadas segun la orientación y une las letras en cada
    casillero para formar la palabra
    :get_palabra() → self._palabra
    :set_palabra(str): actualiza self._palabra
    :definir_puntos(Tablero, dict): recibe el tablero y el diccionario de puntos por letra, recorre cada casillero y
    devuelve los puntos de la palabra → int
    :evaluar_palabra(Tabero, dict, dict): recibe el tablero, el diccionario de palabras válidas y el diccionario de
    puntos por letra. Evalua si la palabra ingresada es válida y calcula el puntaje. Si no es válida la palabra devuelve
    100, sino el devulelve el puntaje → int
    :limpiar(): limpia o vacía todos los valores de turno
    :get_orientacion() → self._orientacion
    :set_letras(str): agrega la letra pasada por parametro a self._letras
    :get_letras() → self._letras
    :add_atril_usada(int): agrega el numero pasado a las claves del atril usadas
    :get_atril_usadas() → self._atril_usadas
    :es_turno_usuario() → self._turno_usuario
    :set_turno_usuario(bool): actualiza self._turno_usuario
    :set_puntaje(int): actualiza self._puntaje
    :add_lista_palabras(str, int, str): recibe la palabra, los puntos y el nombre del jugador y los agrega a
    self._lista_palabras
    :get_lista_palabras(): devuelve la lista palabras como un string → str
    :guardar_lista_palabras() → self._lista_palabras
    :set_lista_palabras(str[]): actualiza self._lista_palabras
    :reinicio(str): cambia el estado de self._turno_usuario, agrega la nueva palabra jugada a self._lista_palabras y
    reinicia las variables de turno
    """

    def __init__(self):
        self._letras = ""
        self._palabra = ""
        self._casilleros_usados = set()
        self._letra_actual = ""
        self._atril_usadas = []
        self._pos_actual = ""
        self._orientacion = ""
        self._turno_usuario = True
        self._lista_palabras = []
        self._puntaje = 0
        self._primer_turno = True

    # Primer Turno
    def get_primer_turno(self):
        return self._primer_turno

    def jugue_primer_turno(self):
        self._primer_turno = False

    def validar_turno(self):
        if self._primer_turno:
            if (7, 7) in self._casilleros_usados:
                return True
            else:
                return False
        else:
            return True

    # Letra Actual
    def set_letra_actual(self, letra):
        self._letra_actual = letra

    def get_letra_actual(self):
        return self._letra_actual

    # Pos Actual
    def set_pos_actual(self, pos):
        self._pos_actual = pos

    def get_pos_actual(self):
        return self._pos_actual

    # Casilleros usados
    def agregar_casillero(self, pos):
        self._casilleros_usados.add(pos)
        if len(self._casilleros_usados) == 2:
            casilleros = list(self._casilleros_usados)
            if casilleros[0][0] == casilleros[1][0]:
                self._orientacion = "horizontal"
            elif casilleros[0][1] == casilleros[1][1]:
                self._orientacion = "vertical"
            else:
                self._orientacion = "no valida"

    def sacar_casillero(self, pos):
        self._casilleros_usados.discard(pos)

    def get_casilleros_usados(self):
        return list(self._casilleros_usados)

    def set_casilleros_usados(self, c):
        self._casilleros_usados = c

    # PALABRA
    def definir_palabra(self, matriz):
        if self._orientacion != "no valida":
            if self._orientacion == "horizontal":
                self._casilleros_usados = sorted(self._casilleros_usados, key=lambda tupla: tupla[1])
                base = self._casilleros_usados[0][1]
                for pos in self._casilleros_usados[1:]:
                    if pos[1] != base + 1:
                        return "_novalido_"
                    base = pos[1]
            elif self._orientacion == "vertical":
                self._casilleros_usados = sorted(self._casilleros_usados, key=lambda tupla: tupla[0])
                base = self._casilleros_usados[0][0]
                for pos in self._casilleros_usados[1:]:
                    if pos[0] != base + 1:
                        return "_novalido_"
                    base = pos[0]
            for pos in self._casilleros_usados:
                self._palabra = self._palabra + matriz[pos[0]][pos[1]].get_letra()
        else:
            return "_novalido_"

    def get_palabra(self):
        return self._palabra

    def set_palabra(self, p):
        self._palabra = p

    # EVALUAR PALABRA
    def definir_puntos(self, matriz, puntos):
        puntaje = 0
        for pos in self._casilleros_usados:
            puntaje = puntaje + matriz[pos[0]][pos[1]].devolver_puntos(puntos, self._palabra)
        self._puntaje = puntaje
        return puntaje

    # -- Cuando termina el turno evalua si la palabra es válida y devuelve el puntaje
    def evaluar_palabra(self, matriz, diccionario, nivel):
        self.definir_palabra(matriz)
        if palabra_es_valida(self._palabra, diccionario, nivel["palabras"]):
            return self.definir_puntos(matriz, nivel["puntos"])
        else:
            return 100

    # Limpiar Valores si se ingresa palabra no valida
    def limpiar(self):
        self._palabra = ""
        self._letras = ""
        self._atril_usadas = []
        self._letra_actual = ""
        self._orientacion = ""
        self._casilleros_usados.clear()
        self._casilleros_usados = set()

    # ORIENTACIÓN
    def get_orientacion(self):
        return self._orientacion

    # Letras
    def set_letras(self, letra):
        self._letras = self._letras + letra

    def get_letras(self):
        return self._letras

    # Usadas atril
    def add_atril_usada(self, num):
        self._atril_usadas.append(num)

    def get_atril_usadas(self):
        return self._atril_usadas

    # Turno
    def es_turno_usuario(self):
        return self._turno_usuario

    def set_turno_usuario(self, va):
        self._turno_usuario = va

    def set_puntaje(self, p):
        self._puntaje = p

    # Lista de palabras
    def add_lista_palabras(self, palabra, puntos, nom):
        dato = nom + " - " + palabra + ": " + str(puntos)
        self._lista_palabras.append(dato)

    def get_lista_palabras(self):
        datos = '\n'.join(self._lista_palabras)
        return datos

    def guardar_lista_palabras(self):
        return self._lista_palabras

    def set_lista_palabras(self, lista):
        self._lista_palabras = lista

    # ReiniciarValores
    def reinicio(self, nom):
        if len(self._palabra) > 0:
            self.add_lista_palabras(self._palabra, self._puntaje, nom)
        self._palabra = ""
        self._letras = ""
        self._letra_actual = ""
        self._orientacion = ""
        self._casilleros_usados.clear()
        self._casilleros_usados = set()
        self._puntaje = 0
        self._atril_usadas.clear()
        if self._turno_usuario:
            self._turno_usuario = False
        else:
            self._turno_usuario = True




