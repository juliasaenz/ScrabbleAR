""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from random import randrange
from datetime import date
import estilo
import PySimpleGUI as sg


class Jugador:
    """
    VARIABLES DE CLASE
    :str[] bolsa: arreglo de letras en el juego

    VARIABLES DE INSTANCIA
    :str _nombre: el nombre del jugador
    :int _puntaje: puntos acumulados en la partida
    :str[] _atril: arreglo de letras en el atril del jugador
    :int cambios: cantidad de cambios posibles del usuario
    :tuple[] _casilleros_usados: posiciones de los casilleros con letras puestas por el usuario

    MÉTODOS
    :dibujar(): dibuja el atril → [sg.Button()]
    :get_nombre() → self._nombre
    :set_puntaje(int): actualiza self._puntaje
    :actualizar_puntaje(int): recibe los puntos del turno y los suma al puntaje general, si el resultado final es negativo deja el puntaje en 0
    :get_puntaje() → self._puntaje
    :armar_atril(): saca 7 letras de la bolsa y las pone en self._bolsa
    :reponer_atril(int[]): recibe el indice de las fichas que debe cambiar, devuelve esas a la bolsa y saca las necesarias para reponer el atril
    :get_atril() → self._atril
    :get_posicion_letra(str): devuelve el indice del atril en el que se encuentra la letra → int
    :sacar_fichas(str[]): recibe arreglo de letras a sacar y las elimina del atril
    :get_ficha(int): devuelve el valor de la ficha en el lugar pasado → str
    :shuffle(str[]): recibe arreglo de letras a sacar del atril, las devuelve a la bolsa y llena el atril → self._cambios
    :get_cambios() → self._cambios
    :get_cant_bolsa(): devuelve la cantidad de fichas que quedan en la bolsa → int
    :add_casilleros_usados(tuple[]): agrega a la lista de casilleros usados los pasados por parámetro
    :fin_de_turno(int,str[],tuple[]): recibe los puntos de la jugada, un arreglo de las fichas usadas, y un arreglo de las posiciones ocupadas y actualiza el puntaje, los casilleros usados y el atril
    :pausar_turno(): crea un diccionario con el nombre, puntaje, casilleros usados y atril del jugador → dict
    :continuar_turno(dict): recibe un diccionario con los datos de la partida y atcualiza el nombre, puntaje, casilleros usados y atril
    :terminar_partida(dict): recorre el atril y le resta al puntaje total el puntaje de cada letra, mientras el puntaje final no sea menor que 0
    :guardar_partida(str): crea un diccionario con el nombre, puntaje, fecha y nivel de la partida → dict
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
        return self._nombre

    # Puntaje
    def set_puntaje(self, pun):
        self._puntaje = pun

    def actualizar_puntaje(self, pun):
        self._puntaje = self._puntaje + pun
        if self._puntaje < 0:
            self._puntaje = 0

    def get_puntaje(self):
        return self._puntaje

    # Atril
    def armar_atril(self):
        while len(Jugador.bolsa) > 0 and len(self._atril) < 7:
            cual = randrange(len(Jugador.bolsa))
            self._atril.append(Jugador.bolsa[cual - 1])
            Jugador.bolsa.pop(cual - 1)

    def reponer_atril(self, usadas):
        for usada in usadas:
            if len(Jugador.bolsa) > 0:
                cual = randrange(len(Jugador.bolsa))
                self._atril[int(usada)] = Jugador.bolsa[cual - 1]
                Jugador.bolsa.pop(cual - 1)
            else:
                print("se terminaron las fichas")

    def get_atril(self):
        return self._atril

    def get_posicion_letra(self, letra):
        return str(self._atril.index(int(letra)))

    # Ficha
    def sacar_fichas(self, fichas):
        for ficha in fichas:
            self._atril.remove(ficha)

    def get_ficha(self, pos):
        try:
            return self._atril[pos]
        except IndexError:
            print("ERROR: en esta posicion ", pos)

    # Shuffle
    def shuffle(self, fichas):
        if self._cambios >= 0:
            for letra in fichas:
                Jugador.bolsa.append(self._atril[int(letra)])
            self.reponer_atril(fichas)
            self._cambios = self._cambios - 1
        return self._cambios

    def get_cambios(self):
        return self._cambios

    # Bolsa
    def get_cant_bolsa(self):
        return len(self.bolsa)

    def add_casilleros_usados(self, cas):
        self._casilleros_usados = self._casilleros_usados + cas

    # Fin de turno
    def fin_de_turno(self, puntos, usadas, cas):
        self.actualizar_puntaje(puntos)
        self.add_casilleros_usados(cas)
        self.reponer_atril(usadas)

    # Pausar Turno
    def pausar_turno(self):
        d_jugador = {"nombre": self._nombre,
                     "puntaje": self._puntaje, "atril": self._atril,
                     "cambios": self._cambios,
                     "casilleros": self._casilleros_usados}
        return d_jugador

    def continuar_turno(self, datos):
        self._atril = datos["atril"]
        self._cambios = datos["cambios"]
        self._puntaje = datos["puntaje"]

    def terminar_partida(self, puntos):
        for letra in self._atril:
            if self._puntaje > 0:
                self._puntaje = self._puntaje - puntos[letra]
            else:
                self._puntaje = 0

    def guardar_partida(self, nivel):
        # Para top 10
        jugador = {
            'nombre': self._nombre,
            'puntaje': self._puntaje,
            'fecha': date.today().strftime("%d/%m/%Y"),
            'nivel': nivel
        }
        return jugador
