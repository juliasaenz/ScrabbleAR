from random import randrange
import PySimpleGUI as sg
import estilo

class Jugador:

    def __init__(self, nom,bolsa):
        self._puntaje = 0
        self._nombre = nom
        self._atril = []
        self.reponer_atril(bolsa)


    #setters y getters
    def set_nombre(self,nom):
        self._nombre = nom

    def set_puntaje(self,puntos):
        self._puntaje = puntos

    def get_nombre(self):
        return self._nombre

    def get_puntaje(self):
        return self._puntaje

    def get_atril(self):
        return self._atril

    #atril
    def reponer_atril(self,bolsa):
        while(len(bolsa) > 0 and len(self._atril) < 7):
            cual = randrange(len(bolsa))
            self._atril.append(bolsa[cual - 1])
            bolsa.pop(cual - 1)
        if (len(bolsa) == 0):
            return False

    def sacar_ficha(self,ficha):
        self._atril.remove(ficha)

    def imprimir_atril(self):
        print(self._atril)

    def fin_de_turno(self):
        print("yay")

    def dibujar(self):
        atril = []
        lista = []
        for letra in self._atril:
            lista.append(sg.Button(letra,key=letra,**estilo.bt))
        atril.append(lista)
        return atril