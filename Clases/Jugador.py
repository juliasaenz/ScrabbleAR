from random import randrange
import estilo
import PySimpleGUI as sg

class Jugador():

    '''
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
    dibujar → dibuja el atril con keys de 0 a 6 → array sg.Button
    '''

    bolsa = []

    def __init__(self,nom):
        self._nombre = nom
        self._puntaje = 0
        self._atril = []
        self._cambios = 3
        self.reponer_atril()

    #DIBUJAR
    def dibujar(self):
        atril = []
        lista = []
        i = 0
        for letra in self._atril:
            lista.append(sg.Button(letra, key = str(i),**estilo.bt,button_color=("black","white")))
            i = i + 1
        atril.append(lista)
        return atril

    #Nombre
    def get_nombre(self):
        return self._nombre

    #Puntaje
    def set_puntaje(self,pun):
        self._puntaje = pun
    def actualizar_puntaje(self,pun):
        self._puntaje = self._puntaje + pun
    def get_puntaje(self):
        return self._puntaje

    #Atril
    def reponer_atril(self):
        while (len(Jugador.bolsa) > 0 and len(self._atril) < 7):
            cual = randrange(len(Jugador.bolsa))
            self._atril.append(Jugador.bolsa[cual - 1])
            Jugador.bolsa.pop(cual - 1)
        if (len(Jugador.bolsa) == 0):
            print("SE TERMINARON LAS FICHAS")
    def get_atril(self):
        return self._atril
    def get_posicion_letra(self,letra):
        return str(self._atril.index(letra))

    #Ficha
    def sacar_fichas(self,fichas):
        for ficha in fichas:
            self._atril.remove(ficha)
    def get_ficha(self,pos):
        return self._atril[pos]

    #Shuffle
    def shuffle(self):
        if (self._cambios >= 0):
            for letra in self._atril:
                Jugador.bolsa.append(letra)
                self._atril.remove(letra)
            self.reponer_atril()
            self._cambios = self._cambios - 1
        return self._cambios
    def get_cambios(self):
        return self._cambios