""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from Clases.Casillero import Casillero


class Tablero:
    """
    Todos los cambios que se quieran a hacer a un Casillero deben hacerse a través de los métodos en Tablero

    :_dimension: Cantidad de casilleros de alto y ancho que tiene el tablero
    :_matriz: Arreglo de Casilleros de tamaño _dimension x _dimension
    :_posiciones: Arreglo de tuplas de posición de tamaño _dimension x _dimension
    :tipos: Arreglo de strings que especifican el tipo de casillero de tamaño _dimension x _dimension
    """

    def __init__(self, tipos):
        self._dimension = 15
        self._matriz = []
        self._posiciones = []
        self._tipos = tipos
        self._iniciar_matriz()
        self.armar_posiciones()

    # DIBUJAR
    def dibujar(self):
        """Devuelve un arreglo de _dimension x _dimension de botones"""
        tablero = []
        for x in range(self._dimension):
            tablero.append([])
            for y in range(self._dimension):
                tablero[x].append(self._matriz[x][y].dibujar((x, y)))
        return tablero

    # Matriz -- iniciar: se hace una vez
    def _iniciar_casillero(self, tipo):
        """Crea un casillero"""
        casilla = Casillero(tipo)
        return casilla

    def _iniciar_matriz(self):
        """ Inicia//Reinicia la matríz en _"""
        for x in range(self._dimension):
            self._matriz.append([])
            for y in range(self._dimension):
                self._matriz[x].append(self._iniciar_casillero(self._tipos[x][y]))

    # Matriz -- actualizar
    def get_matriz(self):
        """ Devuelve el arreglo de la matriz """
        return self._matriz

    def limpiar_matriz(self):
        """ Elimina de la matriz cualquier ficha que no esté bloqueada"""
        for x in range(self._dimension):
            self._matriz.append([])
            for y in range(self._dimension):
                if not self._matriz[x][y].esta_bloqueado():
                    self._matriz[x][y].set_letra("")

    # Posiciones del tablero
    def armar_posiciones(self):
        """ Crea una matriz de tuplas con las posiciones para los botones"""
        for x in range(self._dimension):
            for y in range(self._dimension):
                self._posiciones.append((x, y))

    def get_posiciones(self):
        """ Devuelve la matriz de tuplas de posiciones"""
        return self._posiciones

    # Letra
    def actualizar_casillero(self, letra, pos):
        """ Recibe una letra y una posición y actualiza ese Casillero"""
        self._matriz[pos[0]][pos[1]].set_letra(letra)

    def get_casillero(self, pos):
        """ Recibe una letra y una posición y devuelve ese Casillero"""
        return self._matriz[pos[0]][pos[1]].get_letra()

    # Bloquear casilleros
    def bloquear_casilleros(self, casilleros):
        """ Recibe una letra y una posición y bloquea ese Casillero """
        for pos in casilleros:
            self._matriz[pos[0]][pos[1]].bloquear()

    def esta_bloqueado(self, pos):
        """ Recibe una letra y una posición y devuelve si ese si ese Casillero está bloauqeado"""
        return self._matriz[pos[0]][pos[1]].esta_bloqueado()

    # Pausar Partida
    def pausar_partida(self):
        """ Guarda los valores de la matriz y los devuelve """
        p_matriz = []
        for x in range(self._dimension):
            p_matriz.append([])
            for y in range(self._dimension):
                p_matriz[x].append(self.get_casillero((x, y)))
        return p_matriz

    # continuar
    def continuar_partida(self, arreglo):
        """ Recibe una matriz con los casilleros ocupados y actualiza el Tablero """
        for x in range(self._dimension):
            for y in range(self._dimension):
                if arreglo[x][y] != "":
                    self._matriz[x][y].set_letra(arreglo[x][y])
                    self._matriz[x][y].bloquear()

    def actualizar_tipo(self, pos, tip):
        """ Recibe una letra y una posición y actualiza el tipo de ese Casillero"""
        self._matriz[pos[0]][pos[1]].set_tipo(tip)
