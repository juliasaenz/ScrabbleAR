from Casillero import Casillero
import PySimpleGUI as sg

class Tablero:
    '''Arma el tablero
    Propiedades:
        - dimensiones: por default 15x15
        - matriz: guarda los datos'''

    #Constructor
    def __init__(self):
        self.matriz = []
        self.layout = []
        self.dimensiones = 15
        self.armar_tablero()
        self.dibujar_tablero()

    #Métodos
    def armar_tablero(self):
        ''' Inicia//Reinicia la matríz en _'''
        for x in range(self.dimensiones):
            self.matriz.append([])
            for y in range(self.dimensiones):
                self.matriz[x].append(self.agregar_casillero())

    def agregar_casillero(self):
        '''Crea un casillero'''
        casilla = Casillero("normal")
        return casilla

    def dibujar_tablero(self):
        '''Dibuja el tablero con PySimpleGUI'''
        for z in range(self.dimensiones):
            self.layout.append([])
            for x in range(self.dimensiones):
                self.layout[z].append(sg.Button(self.matriz[x][z].devolver_estado()))
        window = sg.Window("ScrabbleAR").Layout(self.layout)
        button, values = window.Read()

    def imprimir_tablero(self):
        '''Esto es para prueba nuestra sin usar PySimpleGUI'''
        for x in range(self.dimensiones):
            for z in range(self.dimensiones):
                print(self.matriz[x][z].devolver_estado(), end=" ")
            print()

