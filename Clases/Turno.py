""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from Funciones.funciones_palabras import palabra_es_valida


class Turno:
    """
    :_letras: Letras usadas en el turno (sin orden)
    :_palabra: La palabra que se forma
    :_casilleros_usados: Guarda las posiciones de los casilleros usados
    :_letra_actual: Guarda el valor de la letra actual
    :_pos_actual: El último valor del atril presionado
    :_orientacion: La orientación de la palabra
    :_turno_usuario_: True si es el turno del usuario
    :_lista_palabras: Lista de palabras jugadas en el la partida
    :_puntaje: Los puntos de la palabra jugada en el punto
    :primer_turno: True hasta que se juege el primer turno

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
        """ Devuelve si es el primer turno de la partida"""
        return self._primer_turno

    def jugue_primer_turno(self):
        """ Marca el primer turno como jugado"""
        self._primer_turno = False

    def validar_turno(self):
        """ Se fija, si es el primer turno, que haya una ficha en el casillero del medio"""
        if self._primer_turno:
            if (7, 7) in self._casilleros_usados:
                return True
            else:
                return False
        else:
            return True

    # Letra Actual
    def set_letra_actual(self, letra):
        """ Actualiza la última letra del atril seleccionada"""
        self._letra_actual = letra

    def get_letra_actual(self):
        """ Devuelve la última letra del atril seleccionada """
        return self._letra_actual

    # Pos Actual
    def set_pos_actual(self, pos):
        """ Actualiza el último casillero del atril seleccionado """
        self._pos_actual = pos

    def get_pos_actual(self):
        """ Devuelve el último casillero del atril seleccionado"""
        return self._pos_actual

    # Casilleros usados
    def agregar_casillero(self, pos):
        """ Agrega los casilleros usados en el turno, si hay más de dos guardados, calcula la orientación de la
        palabra """
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
        """ Saca el casillero indicado de los casilleros usados"""
        self._casilleros_usados.discard(pos)

    def get_casilleros_usados(self):
        """ Devuelve los casilleros usados"""
        return list(self._casilleros_usados)

    def set_casilleros_usados(self, c):
        """ Actualiza los casilleros usados a una lista pasada por parámetro """
        self._casilleros_usados = c

    # PALABRA
    def definir_palabra(self, matriz):
        """ Según la orientación, ordena los casilleros usados, recupera las letras correspondientes
        y evalua si la palabra es válida"""
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
        """ Devuelve la palabra """
        return self._palabra

    def set_palabra(self, p):
        """ Actualiza la palabra a una pasada por parámetro"""
        self._palabra = p

    # EVALUAR PALABRA
    def definir_puntos(self, matriz, puntos):
        """ Toma los casilleros usados para sumar el puntaje total de la palabra"""
        puntaje = 0
        for pos in self._casilleros_usados:
            puntaje = puntaje + matriz[pos[0]][pos[1]].devolver_puntos(puntos, self._palabra)
        self._puntaje = puntaje
        return puntaje

    # -- Cuando termina el turno evalua si la palabra es válida y devuelve el puntaje
    def evaluar_palabra(self, matriz, diccionario, nivel):
        """ Se fija si la palabra es válida y en ese caso devuelve sus puntos"""
        self.definir_palabra(matriz)
        if palabra_es_valida(self._palabra, diccionario, nivel["palabras"]):
            return self.definir_puntos(matriz, nivel["puntos"])
        else:
            return 100

    # Limpiar Valores si se ingresa palabra no valida
    def limpiar(self):
        """ Reinicia todas las variables del turno """
        self._palabra = ""
        self._letras = ""
        self._atril_usadas = []
        self._letra_actual = ""
        self._orientacion = ""
        self._casilleros_usados.clear()
        self._casilleros_usados = set()

    # ORIENTACIÓN
    def get_orientacion(self):
        """ Devuelve la orientación de la palabra"""
        return self._orientacion

    # Letras
    def set_letras(self, letra):
        """ Actualiza las letras usadas """
        self._letras = self._letras + letra

    def get_letras(self):
        """ Devuelve las letras usadas """
        return self._letras

    # Usadas atril
    def add_atril_usada(self, num):
        """ Agrega a un arreglo las letras del atril usadas """
        self._atril_usadas.append(num)

    def get_atril_usadas(self):
        """ Devuelve las letras del atril usadas"""
        return self._atril_usadas

    # Turno
    def es_turno_usuario(self):
        """ Devuelve si es el turno del usuario"""
        return self._turno_usuario

    def set_turno_usuario(self, va):
        """ Actualiza si es el turno del usuario """
        self._turno_usuario = va

    def set_puntaje(self, p):
        """ Actualiza el puntaje con un valor pasado por parámetro """
        self._puntaje = p

    # Lista de palabras
    def add_lista_palabras(self, palabra, puntos, nom):
        """ Agrega una palabra, su puntaje y quién la jugó a la lista de palabras jugadas """
        dato = nom + " - " + palabra + ": " + str(puntos)
        self._lista_palabras.append(dato)

    def get_lista_palabras(self):
        """ Devuelve la lista de palabras usadas como texto"""
        datos = '\n'.join(self._lista_palabras)
        return datos

    def guardar_lista_palabras(self):
        """ Devuelve la lista de palabras"""
        return self._lista_palabras

    def set_lista_palabras(self, lista):
        """ Actualiza la lista de palabras con una lista pasada por parámetro"""
        self._lista_palabras = lista

    # ReiniciarValores
    def reinicio(self, nom):
        """ Agrega la palabra jugada a la lista, reinicia los valores de turno y actualiza de quién es el turno """
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




