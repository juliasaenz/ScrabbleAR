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

        # getters y setters
        def get_matriz(self):
            return self._matriz

        def llenar_casillero(self, pos, letra):
            self._matriz[pos].ocupar_casillero(letra)

        def vaciar_casillero(self, pos, letra):
            self._matriz[pos].vaciar_casillero(letra)

    #setters y getters
    def get_matriz(self):
        return self._matriz

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

    def ocupar_casillero(self,letra,pos):
        self._matriz[pos[0]][pos[1]].ocupar_casillero(letra)

    def vaciar_casillero(self,pos):
        letra_vieja = self._matriz[pos[0]][pos[1]].vaciar_casillero()
        return letra_vieja

    def casillero_ocupado(self,pos):
        '''Chequear si el casillero en una posicion esta ocupado'''
        return self._matriz[pos[0]][pos[1]].esta_ocupado()

    def intercambio(self,letra,pos):
        letra_vieja = self._matriz[pos[0]][pos[1]].get_letra
        self._matriz[pos[0]][pos[1]].ocupar_casillero(letra)
        print("letra vieja: ",letra_vieja)
        return letra_vieja

    def dibujar(self):
        '''Dibuja el tablero con PySimpleGUI'''
        tablero = []
        for z in range(self._dimensiones):
            tablero.append([])
            for x in range(self._dimensiones):
                tablero[z].append(self._matriz[z][x].dibujar((z,x)))
        return tablero

    def referencia_a_botones(self):
        ''' Devuelve una lista con las tuplas de posiciones
        lo usamos para controlar qué botones se tocan'''
        boton = []
        for x in range(15):
            for y in range(15):
                boton.append((x, y))
        return boton

    def imprimir_tablero(self):
        '''Esto es para prueba nuestra sin usar PySimpleGUI'''
        for x in range(self._dimensiones):
            for z in range(self._dimensiones):
                print(self._matriz[x][z].get_letra(), end=" ")
            print()

