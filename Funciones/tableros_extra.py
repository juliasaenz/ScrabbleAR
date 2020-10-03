""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from random import randrange


class Celda:

    """
    :estado: Puede ser 1 o 0
    :_estado_futuro: Guarda cual será el próximo estado de la Celda
    """

    def __init__(self, estado=randrange(0, 2)):
        self._estado_futuro = 0
        self.estado = estado

    def actualizar_celda(self, celdas, i, j):
        """ Actualiza el estado_futuro de la celda según el estado de sus vecinas """
        vivas = 0
        for c_i in range(i - 1, i + 2):
            for c_j in range(j - 1, j + 2):
                if 0 < i < 14 and 0 < j < 14:
                    if celdas[c_i][c_j].estado == 1 and (i != c_i or j != c_j):
                        vivas = vivas + 1
        if self.estado == 1:
            if vivas < 2:
                self._estado_futuro = 0
            elif vivas < 4:
                self._estado_futuro = 1
            else:
                self._estado_futuro = 0
        else:
            if vivas == 3:
                self._estado_futuro = 1

    def recargar(self):
        """ Pasa su estado_futuro a su estado actual """
        self.estado = self._estado_futuro


class JuegoDeLaVida:
    """ Objeto basado en el Juego de la Vida de John Conway para armar tableros generativos"""

    """"
    :celdas: Matriz de Celdas
    """
    def __init__(self):
        self.celdas = []
        self._iniciar_celdas()
        self.armar_celdas()

    def _iniciar_celdas(self):
        """ Arma la matriz de 15x15 """
        for i in range(15):
            self.celdas.append([])
            for j in range(15):
                self.celdas[i].append(4)

    def armar_celdas(self):
        """ Inicia en cada espacio de la matriz una Celda que vale 0 o 1 aleatoriamente
        de forma que el patrón sea doblemente simétrico """
        # simetria
        for i in range(7):
            for j in range(7):
                estado = randrange(0, 2)
                self.celdas[i][j] = Celda(estado)
                self.celdas[14 - i][j] = Celda(estado)
                self.celdas[i][14 - j] = Celda(estado)
                self.celdas[14 - i][14 - j] = Celda(estado)
        # lineas del medio
        for i in range(7):
            estado = randrange(0, 2)
            self.celdas[7][i] = Celda(estado)
            self.celdas[7][14 - i] = Celda(estado)
            self.celdas[i][7] = Celda(estado)
            self.celdas[14 - i][7] = Celda(estado)
        # centro
        self.celdas[7][7] = Celda()

    def imprimir(self):
        """ Imprime el estado de las celdas """
        lin = " 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
        for i in range(15):
            lin = lin + "\n"
            for j in range(15):
                aux = (" " + str(self.celdas[i][j].estado) + " ")
                lin = lin + aux
        print(lin)
        print("\n")

    def actualizar(self):
        """ Actualiza todas las celdas de la matriz y las recarga """
        for i in range(15):
            for j in range(15):
                self.celdas[i][j].actualizar_celda(self.celdas, i, j)
        for i in range(15):
            for j in range(15):
                self.celdas[i][j].recargar()

    def hay_vivas(self):
        """ Devuelve si hay en la matriz más de 20 celdas vivas (que valgan 1) """
        vivas = 0
        for i in range(15):
            for j in range(15):
                vivas = vivas + 1
        return vivas > 20


class Grilla:
    """
    :juegos: Lista de Juegos de La Vida
    :cuantos_necesito: Cual es el máximo número al que necesito llegar en por lo menos una celda
    :cantidad_juegos: Cantidad de Juegos de La Vida que quiero
    :cantidad_epocas: Cantidad de épocas para cada Juego de La Vida
    :_continuar: Si es True, sigue creando Juegos
    """

    def __init__(self, cantidad_juegos_: object, cantidad_epocas_: object) -> object:
        self.juegos = []
        self.cuantos_necesito = 8
        self.cantidad_juegos = cantidad_juegos_
        self.cantidad_epocas = cantidad_epocas_
        self._continuar = False
        self._juegos()

    def hay_suficientes(self):
        """ Se fija si hay por lo menos una celda que, sumando todos los juegos, valga 8 """
        for j in range(len(self.juegos[0].celdas)):
            for k in range(len(self.juegos[0].celdas)):
                cual = 0
                for i in range(len(self.juegos)):
                    if self.juegos[i].celdas[j][k].estado == 1:
                        cual = cual + 1
                if (self.cuantos_necesito - 1) == cual:
                    return True
        return False

    def _juegos(self):
        """ Crea la cantidad de juegos indicada, atraviesa la cantidad de épocas con cada juego indicada y,
        si el juego tiene más de 20 celdas vivas, lo agrega al arreglo de juegos. Si luego de esto no se llegá
        al valor de celda que se busca, se agrega de a un juego al arreglo hasta que se consiga"""
        for i in range(self.cantidad_juegos):
            juego = JuegoDeLaVida()
            for j in range(self.cantidad_epocas):
                juego.actualizar()
            if juego.hay_vivas():
                self.juegos.append(juego)

        self._continuar = self.hay_suficientes()
        failsafe = 0
        while not self._continuar and failsafe < 1000:
            failsafe = failsafe + 1
            juego = JuegoDeLaVida()
            for j in range(self.cantidad_epocas):
                juego.actualizar()
            if juego.hay_vivas():
                self.juegos.append(juego)
            self._continuar = self.hay_suficientes()

    def imprimir(self):
        """ Imprime la grilla final """
        print(" --- GRILLA FINAL --- ")
        lin = ""
        for j in range(len(self.juegos[0].celdas)):
            lin = lin + "\n"
            for k in range(len(self.juegos[0].celdas)):
                cual = 0
                for i in range(len(self.juegos)):
                    if self.juegos[i].celdas[j][k].estado == 1:
                        cual = cual + 1
                try:
                    aux = (" " + str(cual) + " ")
                except AttributeError:
                    aux = (" " + str(99) + " ")
                lin = lin + aux
        print(lin)

    def _sumar(self, i, j):
        """ Suma todas las celdas en la misma posición de todos los juegos """
        num = 0
        for juego in self.juegos:
            num = num + juego.celdas[i][j].estado
        return num

    def _cambiar(self, num):
        """ Reinterpreta cada número como un string que indique el tipo de Casillero """
        if num == 1:
            return "doble_letra"
        elif num == 2:
            return "menos_uno"
        elif num == 3:
            return "triple_letra"
        elif num == 4:
            return "menos_dos"
        elif num == 0:
            return "normal"
        elif num == 5:
            return "doble_palabra"
        elif num == 6:
            return "menos_tres"
        elif num == 7:
            return "triple_palabra"

    def grilla_final(self):
        """ Traduce toda la grilla final de números a strings de tipo de Casillero y devuelve esa matriz """
        final = []
        for i in range(15):
            final.append([])
            for j in range(15):
                final[i].append(self._sumar(i, j))
                final[i][j] = self._cambiar(final[i][j])
        return final


def tablero_aleatorio():
    """ Genera un trablero aleatorio"""
    grilla = Grilla(7, 8)
    return grilla.grilla_final()
