""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from Clases.Jugador import Jugador
import PySimpleGUI as sg
import itertools as it
from Funciones.funciones_palabras import palabra_es_valida
import estilo
from random import randrange


class Computadora(Jugador):
    """
    Extiende → Jugador por lo que tiene todos sus variables y métodos

    VARIABLES DE INSTANCIA
    :str _palabra: guarda la palabra elegida por la computadora cada turno
    :tuple[] _casilleros: arreglo de posiciones de los casilleros usados en el turno
    :str[] _atril_usadas:arreglo de las letras usadas del atril
    :int _puntos: puntos acumulados en un turno
    :int _max: longitud de la palabra mas larga posible en un turno

    MÉTODOS :dibujar(): dibuja el atril → [sg.Button()] :_reponer_atril(): reemplaza las fichas del atril usadas
    :_sacar_fichas(): saca del atril las letras usadas en la palabra final :sacar_y_reponer_atril()_: actualiza el
    atril, y las variables de turno (self._palabra, self._puntos, self._max) :get_palabra() → self._palabra
    :get_puntaje_palabra() → self._puntos :get_casilleros() → self._casilleros :_armar_palabra(dict,int[],
    str): recibe un diccionario de palabras válidas, el arreglo de categorias de palabras válido y el nivel. Según el
    nivel devuelve la mejor palabra posible con las fichas del atril :_ubicar_palabra(Tablero, str, boolean,
    dict): recibe el tablero, el nivel, si ya paso el primer turno y el diccionario de puntos por letra y según el
    nivel ubica la palabra. Niveles fácil y medio ubica en una posición aleatoria disponible, en el nivel difícil lo
    ubica en la mejor posición posible. Devuelve los casilleros que usa → self._casilleros :_mejor_opcion(tuple[],
    Casillero[][], dict): recibe un arreglo de posibles posiciones para la palabra, lo ubica en la matriz de
    Casilleros, calcula el puntaje y si es más alto que el guardado actualmente, guarda esa posición
    :_chequear_casilleros(tuple[], tuple, Tablero): recibe una posición e intenta posicionar de forma horizontal la
    palabra en el Tablero :definir_puntos(Tablero, dict, tuple[]): recibe el Tablero, el diccionario de puntos y los
    casilleros usados y calcula los puntos de ubicar la palabra en esa posición
    """

    def __init__(self):
        self._palabra = ""
        self._casilleros = []
        self._atril_usadas = []
        self._puntos = 0
        self._max = -1
        super().__init__("Computadora")

    def dibujar(self):
        """ Dibuja el atril de la compu como botones desactivados"""
        atril = []
        lista = []
        for letra in self._atril:
            lista.append(sg.Button(" ", key="compu", **estilo.bt, button_color=("black", "#FAFAFA"), disabled=True))
        atril.append(lista)
        return atril

    def _reponer_atril(self):
        while len(Jugador.bolsa) > 0 and len(self._atril) < 7:
            cual = randrange(len(Jugador.bolsa))
            self._atril.append(Jugador.bolsa[cual - 1])
            Jugador.bolsa.pop(cual - 1)

    def _sacar_fichas(self):
        for letra in self._palabra:
            self._atril.remove(letra)

    def sacar_y_reponer_atril(self):
        self._sacar_fichas()
        self._reponer_atril()
        self._palabra = ""
        self._puntos = 0
        self._max = -1

    # Palabra y puntaje
    def get_palabra(self):
        return self._palabra

    def get_puntaje_palabra(self):
        return self._puntos

    def get_casilleros(self):
        return self._casilleros

    # ------ Armar palabras

    def _armar_palabra(self, diccionario, tipos, dificultad):
        """ Devuelve la palabra que puede formar con el atril, dependiendo del nivel
        - Fácil: la mejor palabra de máximo 5 letras
        - Medio y difícil: la mejor palabra de máximo 7 letras """
        palabras = set()
        if dificultad == "facil":
            for i in range(2, len(self._atril) + 1):
                palabras.update((map("".join, it.permutations(self._atril, i))))
            for i in palabras:
                # recibe diccionario y tipos de palabras que acepta
                if palabra_es_valida(i, diccionario, tipos):
                    if 6 > len(i) > len(self._palabra):
                        self._palabra = i
        else:
            for i in range(2, len(self._atril) + 1):
                palabras.update((map("".join, it.permutations(self._atril, i))))
            for i in palabras:
                # recibe diccionario y tipos de palabras que acepta
                if palabra_es_valida(i, diccionario, tipos):
                    if len(i) > len(self._palabra):
                        self._palabra = i
        palabras.clear()

    # Busca donde guardar la palabra de la compu
    def _ubicar_palabra(self, matriz, dificultad, primer_turno, puntos):
        """ Devuelve un arreglo de posiciones en los que entra la palabra"""
        casilleros = []
        if primer_turno:
            pos = (7, 7)
            self._chequear_casilleros(casilleros, pos, matriz)
            self._casilleros = casilleros
        else:
            pos = (randrange(15), randrange(15))
            # Se elije una posición al azar en el tablero y se busca si los adyacentes estan disponibles
            if dificultad == "facil" or dificultad == "medio":
                while len(casilleros) != len(self._palabra):
                    casilleros.clear()
                    self._chequear_casilleros(casilleros, pos, matriz)
                    pos = (randrange(15), randrange(15))
                self._casilleros = casilleros
            else:
                for x in range(15):
                    for y in range(15):
                        if not matriz.esta_bloqueado((x, y)):
                            self._chequear_casilleros(casilleros, (x, y), matriz)
                            if len(casilleros) == len(self._palabra):
                                self._mejor_opcion(casilleros, matriz, puntos)
                            casilleros.clear()
                self._puntos = self._max
        self.add_casilleros_usados(self._casilleros)
        return self._casilleros

    def jugada(self, matriz, diccionario, nivel, primer_turno):
        self._armar_palabra(diccionario, nivel["palabras"], nivel["compu"])
        self._ubicar_palabra(matriz, nivel["compu"], primer_turno, nivel["puntos"])

    # Funciones auxiliares para elegir la posición
    def _mejor_opcion(self, casilleros, matriz, puntos):
        for p in range(len(self._palabra)):
            matriz.actualizar_casillero(self._palabra[p], casilleros[p])
        punt = self.definir_puntos(matriz.get_matriz(), puntos, casilleros)
        for p in range(len(self._palabra)):
            matriz.actualizar_casillero("", casilleros[p])
        if punt > self._max:
            self._max = punt
            self._casilleros = casilleros.copy()

    def _chequear_casilleros(self, casilleros, pos, matriz):
        """ Busca por la extensión de la palabra si hay suficientes casilleros"""
        if pos[0] < 15 and pos[1] < 15 and len(casilleros) < len(self._palabra) and (not matriz.esta_bloqueado(pos)):
            casilleros.append(pos)
            pos = (pos[0], pos[1] + 1)
            self._chequear_casilleros(casilleros, pos, matriz)

    def definir_puntos(self, matriz, puntos, casilleros):
        puntaje = 0
        for pos in casilleros:
            try:
                puntaje = puntaje + matriz[pos[0]][pos[1]].devolver_puntos(puntos, self._palabra)
            except KeyError:
                print(matriz[pos[0]][pos[1]])
        self._puntos = puntaje
        return puntaje

