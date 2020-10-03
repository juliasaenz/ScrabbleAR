""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from random import randrange
from datetime import date
import estilo
import PySimpleGUI as sg


class Jugador:
    """
    :bolsa: Variable de Clase. Arreglo de letras en el juego

    :_nombre: El nombre del jugador
    :_puntaje: Puntos acumulados en la partida
    :_atril: Arreglo de letras en el atril del jugador
    :cambios: Cantidad de cambios posibles del usuario
    :_casilleros_usados: Posiciones de los casilleros con letras puestas por el usuario

    """

    bolsa = []

    def __init__(self, nom):
        self._nombre = nom
        self._puntaje = 0
        self._atril = []
        self._cambios = 3
        self.armar_atril()
        self._casilleros_usados = []

    # DIBUJAR
    def dibujar(self):
        """ Devuelve un arreglo de botones con las fichas del atril"""
        atril = []
        lista = []
        i = 0
        for letra in self._atril:
            lista.append(sg.Button(letra, key=str(i), **estilo.bt, button_color=("black", "white")))
            i = i + 1
        atril.append(lista)
        return atril

    # Nombre
    def get_nombre(self):
        """ Devuelve el nombre del jugador """
        return self._nombre

    # Puntaje
    def set_puntaje(self, pun):
        """ Setea el puntaje del jugador"""
        self._puntaje = pun

    def actualizar_puntaje(self, pun):
        """ Suma al puntaje total los puntos nuevos acumulados """
        self._puntaje = self._puntaje + pun
        if self._puntaje < 0:
            self._puntaje = 0

    def get_puntaje(self):
        """ Devuelve el puntaje del jugador """
        return self._puntaje

    # Atril
    def armar_atril(self):
        """ Crea el arreglo de 7 fichas aleatorias sacadas de la bolsa"""
        while len(Jugador.bolsa) > 0 and len(self._atril) < 7:
            cual = randrange(len(Jugador.bolsa))
            self._atril.append(Jugador.bolsa[cual - 1])
            Jugador.bolsa.pop(cual - 1)

    def reponer_atril(self, usadas):
        """ Repone el atril según la cantidad de fichas que se hayan usado en el turno """
        for usada in usadas:
            if len(Jugador.bolsa) > 0:
                cual = randrange(len(Jugador.bolsa))
                self._atril[int(usada)] = Jugador.bolsa[cual - 1]
                Jugador.bolsa.pop(cual - 1)
            else:
                print("se terminaron las fichas")

    def get_atril(self):
        """ Devuelve las fichas del atril"""
        return self._atril

    def get_posicion_letra(self, letra):
        """ Devuelve la posición en el atril de una letra"""
        return str(self._atril.index(int(letra)))

    # Ficha
    def sacar_fichas(self, fichas):
        """ Saca una ficha del atril"""
        for ficha in fichas:
            self._atril.remove(ficha)

    def get_ficha(self, pos):
        """ Devuelve la ficha correspondiente a una posición del atril"""
        try:
            return self._atril[pos]
        except IndexError:
            print("ERROR: en esta posicion ", pos)

    # Shuffle
    def shuffle(self, fichas):
        """ Elimina las letras seleccionadas del atril y repone con fichas aleatorias de la bolsa"""
        if self._cambios >= 0:
            for letra in fichas:
                Jugador.bolsa.append(self._atril[int(letra)])
            self.reponer_atril(fichas)
            self._cambios = self._cambios - 1
        return self._cambios

    def get_cambios(self):
        """ Devuelve la cantidad de cambios hechos en la partida"""
        return self._cambios

    # Bolsa
    def get_cant_bolsa(self):
        """ Devuelve la cantidad de fichas en la bolsa"""
        return len(self.bolsa)

    def add_casilleros_usados(self, cas):
        """ Agrega a un arreglo la posición de un casillero"""
        self._casilleros_usados = self._casilleros_usados + cas

    # Fin de turno
    def fin_de_turno(self, puntos, usadas, cas):
        """ Actualiza el puntaje, agrega los casilleros usados y repone el atril"""
        self.actualizar_puntaje(puntos)
        self.add_casilleros_usados(cas)
        self.reponer_atril(usadas)

    # Pausar Turno
    def pausar_turno(self):
        """ Guarda y devuelve el nombre, puntaje, atril, cambios y casilleros usados del jugador """
        d_jugador = {"nombre": self._nombre,
                     "puntaje": self._puntaje, "atril": self._atril,
                     "cambios": self._cambios,
                     "casilleros": self._casilleros_usados}
        return d_jugador

    def continuar_turno(self, datos):
        """ Recibe y actualiza el puntaje, cambios y atril del jugador"""
        self._atril = datos["atril"]
        self._cambios = datos["cambios"]
        self._puntaje = datos["puntaje"]

    def terminar_partida(self, puntos):
        """ Resta del puntaje total el valor de las fichas en el atril """
        for letra in self._atril:
            if self._puntaje > 0:
                self._puntaje = self._puntaje - puntos[letra]
            else:
                self._puntaje = 0

    def guardar_partida(self, nivel):
        """ Guarda y devuelve el nombre y puntaje del jugador, la fecha actual y el nivel al que jugó"""
        # Para top 10
        jugador = {
            'nombre': self._nombre,
            'puntaje': self._puntaje,
            'fecha': date.today().strftime("%d/%m/%Y"),
            'nivel': nivel
        }
        return jugador
