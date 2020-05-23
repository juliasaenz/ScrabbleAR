from Casillero import Casillero
class Tablero:
    '''Arma el tablero
    Propiedades:
        - dimensiones: por default 15x15'''

    #Constructor
    def __init__(self):
        self.matriz = []
        self.dimensiones = 15
        self.armar_tablero()

    #Métodos
    def armar_tablero(self):
        ''' Inicia//Reinicia la matríz en _'''
        for x in range(self.dimensiones):
            self.matriz.append([])
            for y in range(self.dimensiones):
                self.matriz[x].append(self.agregarCasillero())

    def agregarCasillero(self):
        '''Crea un casillero'''
        casilla = Casillero("normal")
        return casilla

    def dibujar_tablero(self):
        '''Dibuja el tablero con PySimpleGUI'''

    def imprimir_tablero(self):
        '''Esto es para prueba nuestra sin usar PySimpleGUI'''
        for x in range(self.dimensiones):
            for z in range(self.dimensiones):
                print(self.matriz[x][z].devolver_estado(), end=" ")
            print()

