""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from random import randrange
from datetime import date
import estilo
import PySimpleGUI as sg


class Jugador:
    """
    VARIABLES DE CLASE
    bolsa: array str → todas las letras a usar en el juego

    VARIABLES
    _nombre: str → el nombre de un jugador
    _puntaje: int → el puntaje del jugador
    _atril: str array → las fichas en el atril
    _cambios: int → los cambios que puede hacer

    MÉTODOS
    get_nombre: devuelve _nombre del jugador → str
    set_puntaje: cambia _puntaje del jugador
    get_puntaje: devuelve _puntaje → int
    actualizar_puntaje: suma a _puntaje el valor pasado
    reponer_atril: llena el arreglo _atril con letras de bolsa hasta tener 7
    get_atril: devuelve el _atril → array int
    get_posicion_letra: como el arreglo va de 0 a 6, se le pasa la letra y devuelve la posición en la que está
    shuffle: cambia todas las letras del atril y resta la cantidad de cambios posibles
    get_cambios: devuelve _cambios → int
    dibujar: dibuja el atril con keys de 0 a 6 → array sg.Button
    pausar_turno: guarda los valores de las variables de instancia en un diccionario → diccionario
    continuar: actualiza las variables de instancia con los valores pasados por parametro
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

        '''while (len(Jugador.bolsa) > 0 and len(self._atril) < 7):
            cual = randrange(len(Jugador.bolsa))
            self._atril.append(Jugador.bolsa[cual - 1])
            Jugador.bolsa.pop(cual - 1)
        if (len(Jugador.bolsa) == 0):
            print("SE TERMINARON LAS FICHAS")'''

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

    # Fin de turno
    def fin_de_turno(self, puntos, usadas, cas):
        self.actualizar_puntaje(puntos)
        self.add_casilleros_usados(cas)
        self.reponer_atril(usadas)

    def add_casilleros_usados(self, cas):
        self._casilleros_usados = self._casilleros_usados + cas

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

    def guardar_partida(self, nivel):
        jugador = {
            'nombre': self._nombre,
            'puntaje': self._puntaje,
            'fecha': date.today().strftime("%d/%m/%Y"),
            'nivel: ': nivel
        }
        return jugador
