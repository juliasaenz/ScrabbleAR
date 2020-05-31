from Clases.Casillero import Casillero
import PySimpleGUI as sg
import estilo

class Tablero:
    '''Arma el tablero
    Propiedades:
        - dimensiones: por default 15x15
        - matriz: el tablero'''

    #Constructor
    def __init__(self):
        self._matriz = []
        self._dimensiones = 15
        self.armar_tablero()
        #self.dibujar_tablero()

    #Métodos
    def armar_tablero(self):
        ''' Inicia//Reinicia la matríz en _'''
        for x in range(self._dimensiones):
            self._matriz.append([])
            for y in range(self._dimensiones):
                self._matriz[x].append(self.agregar_casillero())


    def agregar_casillero(self):
        '''Crea un casillero'''
        casilla = Casillero("normal")
        return casilla

    def dibujar(self):
        '''Dibuja el tablero con PySimpleGUI'''
        tablero = []
        num = 0
        for z in range(self._dimensiones):
            tablero.append([])
            for x in range(self._dimensiones):
                clave = ( z, x)
                tablero[z].append(self._matriz[z][x].dibujar(clave))

        return tablero

    def imprimir_tablero(self):
        '''Esto es para prueba nuestra sin usar PySimpleGUI'''
        for x in range(self._dimensiones):
            for z in range(self._dimensiones):
                print(self._matriz[x][z].devolver_estado(), end=" ")
            print()

