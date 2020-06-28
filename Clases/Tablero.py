import PySimpleGUI as sg
from random import randrange
from Clases.Casillero import Casillero

class Tablero:

    '''

    VARIABLES
    _dimension: int → la dimensión del tablero
    _matriz: array Casillero→ arreglo de Casilleros
    _posiciones: array tuple → arreglo de tuplas de posición
    _tipos: array str → arreglo de str de tipos

    MÉTODOS
    iniciar_casillero: crea un objeto casillero → Casillero
    iniciar_matriz: llena _matriz de casilleros
    actualizar_casillero: cambia el valor de _letra del casillero indicado
    get_casillero: devuelve el valor de letra en el casillero indicado → str
    get_matriz: devuelve la _matriz de casilleros → array Casillero
    limpiar_matriz: resetea todos los casilleros no bloqueados
    armar_posiciones: lllena _posiciones con las tuplas de posición
    get_posiciones: devuelve el arreglo de posiciones → array tuple
    bloquear_casillero: bloquear en el casillero indicado pasa a True
    esta_bloqueado: devuelve si el casillero está bloqueado → bool
    dibujar: dibuja el tablero de botones → array sg.Button

    ACLARACIÓN IMPORTANTE
    Todos los cambios a Casilleros, hacerlo mediante métodos de Tablero
    '''

    def __init__(self,tipos):
        self._dimension = 15
        self._matriz = []
        self._posiciones = []
        self._tipos = tipos
        self._iniciar_matriz()
        self.armar_posiciones()

    #DIBUJAR
    def dibujar(self):
        '''Dibuja el tablero con PySimpleGUI'''
        tablero = []
        for x in range(self._dimension):
            tablero.append([])
            for y in range(self._dimension):
                tablero[x].append(self._matriz[x][y].dibujar((x,y)))
        return tablero

    #Matriz -- iniciar: se hace una vez
    def _iniciar_casillero(self,tipo):
        '''Crea un casillero'''
        casilla = Casillero(tipo)
        return casilla
    def _iniciar_matriz(self):
        ''' Inicia//Reinicia la matríz en _'''
        for x in range(self._dimension):
            self._matriz.append([])
            for y in range(self._dimension):
                self._matriz[x].append(self._iniciar_casillero(self._tipos[randrange(len(self._tipos)-1)]))

    #Matriz -- actualizar
    def actualizar_casillero(self,letra,pos):
        self._matriz[pos[0]][pos[1]].set_letra(letra)
    def get_casillero(self,pos):
        return self._matriz[pos[0]][pos[1]].get_letra()

    def get_matriz(self):
        return self._matriz
    def limpiar_matriz(self):
        for x in range(self._dimension):
            self._matriz.append([])
            for y in range(self._dimension):
                if(not self._matriz[x][y].esta_bloqueado()):
                    self._matriz[x][y].set_letra("")

    #Posiciones del tablero
    def armar_posiciones(self):
        ''' Matriz de posiciones para los botones'''
        for x in range(self._dimension):
            for y in range(self._dimension):
                self._posiciones.append((x, y))

    def get_posiciones(self):
        return self._posiciones

    #Bloquear casilleros
    def bloquear_casilleros(self,casilleros):
        for pos in casilleros:
            self._matriz[pos[0]][pos[1]].bloquear()
    def esta_bloqueado(self,pos):
        return self._matriz[pos[0]][pos[1]].esta_bloqueado()

    # Pausar Partida
    def pausar_partida(self):
        p_matriz = []
        for x in range(self._dimension):
            p_matriz.append([])
            for y in range(self._dimension):
                p_matriz[x].append(self.get_casillero((x,y)))
        return p_matriz

    #continuar
    def continuar_partida(self,arreglo):
        for x in range(self._dimension):
            for y in range(self._dimension):
                if(arreglo[x][y] != ""):
                    self._matriz[x][y].set_letra(arreglo[x][y])
                    self._matriz[x][y].bloquear()