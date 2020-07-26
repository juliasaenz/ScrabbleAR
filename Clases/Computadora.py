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

    VARIABLES

    _palabra: str → la palabra que va a jugar
    _casilleros array tuple → el arreglo de tuplas de posición en las que se va a dibujar la palabra

    MÉTODOS
    armar_palabra: con las fichas de su atril, guarda la palabra más larga posible en _palabra
    get_palabra: devuelve _palabra → str
    ubicar_palabra: recibe la matriz de Tablero, elige una posición al azar, se fija que no este bloqueada y luego si sus adyacentes están libres. Devuelve arreglo de tuplas → array tuple
    _chequear_casilleros: recibe un casillero y la matriz de Tablero y se fija si todos los casilleros adyacentes estan libres
    get_casilleros: devuelve _casilleros → array tuple
    devolver_palabra: devuelve la palabra generada → str
    dibujar: dibuja arreglo de botones desactivados → array sg.Button
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

    def reponer_atril(self):
        while len(Jugador.bolsa) > 0 and len(self._atril) < 7:
            cual = randrange(len(Jugador.bolsa))
            self._atril.append(Jugador.bolsa[cual - 1])
            Jugador.bolsa.pop(cual - 1)

    def sacar_y_reponer_atril(self):
        self.sacar_fichas()
        self.reponer_atril()
        self._palabra = ""
        self._puntos = 0
        self._max = -1

    def sacar_fichas(self):
        # print("asi estaba el atril: ", self.get_atril())
        for letra in self._palabra:
            try:
                self._atril.remove(letra)
            except ValueError:
                print("esta letra me esta causando problemas: ", letra)

    def get_palabra(self):
        return self._palabra

    def get_puntaje_palabra(self):
        return self._puntos

    # ------ Armar palabras

    def armar_palabra(self, diccionario, tipos, dificultad):
        """ Devuelve la palabra más larga que puede formar con el atril"""
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
    def ubicar_palabra(self, matriz, dificultad, primer_turno, puntos):
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
                                # print("Opcion: ", casilleros, "pal: ", self._palabra)
                                self.mejor_opcion(casilleros, matriz, puntos)
                            casilleros.clear()
                self._puntos = self._max
                print("fin: ", self._casilleros)
        return self._casilleros

    def mejor_opcion(self, casilleros, matriz, puntos):
        for p in range(len(self._palabra)):
            matriz.actualizar_casillero(self._palabra[p], casilleros[p])
        punt = self.definir_puntos(matriz.get_matriz(), puntos, casilleros)
        for p in range(len(self._palabra)):
            matriz.actualizar_casillero("", casilleros[p])
        if punt > self._max:
            # print("este esta mejor: ", punt, " - ", self._max, " ", casilleros, " ", self._palabra)
            self._max = punt
            self._casilleros = casilleros.copy()

    def _chequear_casilleros(self, casilleros, pos, matriz):
        """ Busca por la extensión de la palabra si hay suficientes casilleros"""
        if pos[0] < 15 and pos[1] < 15 and len(casilleros) < len(self._palabra) and (not matriz.esta_bloqueado(pos)):
            casilleros.append(pos)
            pos = (pos[0], pos[1] + 1)
            self._chequear_casilleros(casilleros, pos, matriz)

    def get_casilleros(self):
        return self._casilleros

    def definir_puntos(self, matriz, puntos, casilleros):
        puntaje = 0
        for pos in casilleros:
            try:
                puntaje = puntaje + matriz[pos[0]][pos[1]].devolver_puntos(puntos, self._palabra)
            except KeyError:
                print(matriz[pos[0]][pos[1]])
        # print("puntaje: ", puntaje)
        self._puntos = puntaje
        print("puntos compu: ", self._puntos)
        return puntaje

    def jugada(self, matriz, diccionario, nivel, primer_turno):
        self.armar_palabra(diccionario, nivel["palabras"], nivel["compu"])
        self.ubicar_palabra(matriz, nivel["compu"], primer_turno, nivel["puntos"])
