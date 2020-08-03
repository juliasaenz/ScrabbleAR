""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

import PySimpleGUI as sg
from random import randrange
from Clases.Casillero import Casillero


class Tablero:
    """
    VARIABLES DE INSTANCIA
    :int _dimension: cantidad de casilleros de alto y ancho que tiene el tablero
    :Casillero[][] _matriz: arreglo de casilleros de tamaño _dimension x _dimension
    :tuple[][] _posiciones: arreglo de tuplas de posición de tamaño _dimension x _dimension
    :str[][] tipos: arreglo de strings que especifican el tipo de casillero de tamaño _dimension x _dimension

    MÉTODOS
    :dibujar(clave): devuelve un arreglo de _dimension x _dimension de Casilleros → [sg.Button()]
    :_iniciar_casillero(str): recibe el tipo de casillero y crea un casillero → Casillero
    :_iniciar_matriz(): llena a self._matriz con Casilleros
    :get_matriz() → self._matriz
    :limpiar_matriz(): resetea todos los casilleros no bloqueados
    :armar_posiciones(): llena self._posiciones
    :get_posiciones() → self._posiciones
    :actualizar_casillero(str, tuple): recibe la letra y posición del casillero y lo actualiza con el nuevo valor
    :get_casillero(tuple): recibe una posicion y devuelve la letra en el casillero correspondiente → str
    :bloquear_casilleros(tuple[]): bloquea los casilleros con las posiciones pasadas
    :esta_bloqueado(tuple): recibe posición y devuelve si ese casillero esta bloqueado → bool
    :pausar_partida: guarda todos valores de los casilleros en una matriz y la devuelve → str[][]
    :continuar_partida(str[][]): recibe un arreglo del tamaño del tablero y para cada letra, ocupa el Casillero correspondiente y lo bloquea
    :actualizar_tipo(tuple, str): recibe una posición y un nuevo tipo y actualiza el casillero correspondiente

    ACLARACIÓN IMPORTANTE
    Todos los cambios a Casilleros, hacerlo mediante métodos de Tablero
    """

    def __init__(self, tipos):
        self._dimension = 15
        self._matriz = []
        self._posiciones = []
        self._tipos = tipos
        self._iniciar_matriz()
        self.armar_posiciones()

    # DIBUJAR
    def dibujar(self):
        """Dibuja el tablero con PySimpleGUI"""
        tablero = []
        for x in range(self._dimension):
            tablero.append([])
            for y in range(self._dimension):
                tablero[x].append(self._matriz[x][y].dibujar((x, y)))
        return tablero

    # Matriz -- iniciar: se hace una vez
    def _iniciar_casillero(self, tipo):
        """Crea un casillero"""
        casilla = Casillero(tipo)
        return casilla

    def _iniciar_matriz(self):
        """ Inicia//Reinicia la matríz en _"""
        for x in range(self._dimension):
            self._matriz.append([])
            for y in range(self._dimension):
                self._matriz[x].append(self._iniciar_casillero(self._tipos[x][y]))

    # Matriz -- actualizar
    def get_matriz(self):
        return self._matriz

    def limpiar_matriz(self):
        for x in range(self._dimension):
            self._matriz.append([])
            for y in range(self._dimension):
                if not self._matriz[x][y].esta_bloqueado():
                    self._matriz[x][y].set_letra("")

    # Posiciones del tablero
    def armar_posiciones(self):
        """ Matriz de posiciones para los botones"""
        for x in range(self._dimension):
            for y in range(self._dimension):
                self._posiciones.append((x, y))

    def get_posiciones(self):
        return self._posiciones

    # Letra
    def actualizar_casillero(self, letra, pos):
        self._matriz[pos[0]][pos[1]].set_letra(letra)

    def get_casillero(self, pos):
        return self._matriz[pos[0]][pos[1]].get_letra()

    # Bloquear casilleros
    def bloquear_casilleros(self, casilleros):
        for pos in casilleros:
            self._matriz[pos[0]][pos[1]].bloquear()

    def esta_bloqueado(self, pos):
        return self._matriz[pos[0]][pos[1]].esta_bloqueado()

    # Pausar Partida
    def pausar_partida(self):
        p_matriz = []
        for x in range(self._dimension):
            p_matriz.append([])
            for y in range(self._dimension):
                p_matriz[x].append(self.get_casillero((x, y)))
        return p_matriz

    # continuar
    def continuar_partida(self, arreglo):
        for x in range(self._dimension):
            for y in range(self._dimension):
                if arreglo[x][y] != "":
                    self._matriz[x][y].set_letra(arreglo[x][y])
                    self._matriz[x][y].bloquear()

    def actualizar_tipo(self, pos, tip):
        self._matriz[pos[0]][pos[1]].set_tipo(tip)
