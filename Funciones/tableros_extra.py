""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

from random import randrange


class Celda:

    def __init__(self, estado=randrange(0, 2)):
        self._estado_futuro = 0
        self.estado = estado

    def actualizar_celda(self, celdas, i, j):
        """ Actualiza el estado de la celda """
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
        self.estado = self._estado_futuro


class JuegoDeLaVida:

    def __init__(self):
        self.celdas = []
        self._iniciar_celdas()
        self.armar_celdas()

    def _iniciar_celdas(self):
        """ iniciar la celda en 0 """
        for i in range(15):
            self.celdas.append([])
            for j in range(15):
                self.celdas[i].append(4)

    def armar_celdas(self):
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
        lin = " 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
        for i in range(15):
            lin = lin + "\n"
            for j in range(15):
                aux = (" " + str(self.celdas[i][j].estado) + " ")
                lin = lin + aux
        print(lin)
        print("\n")

    def actualizar(self):
        for i in range(15):
            for j in range(15):
                self.celdas[i][j].actualizar_celda(self.celdas, i, j)
        for i in range(15):
            for j in range(15):
                self.celdas[i][j].recargar()

    def hay_vivas(self):
        vivas = 0
        for i in range(15):
            for j in range(15):
                vivas = vivas + 1
        return vivas > 20


class Grilla:

    def __init__(self, cantidad_juegos_: object, cantidad_epocas_: object) -> object:
        self.juegos = []
        self.cuantos_necesito = 8
        self.cantidad_juegos = cantidad_juegos_
        self.cantidad_epocas = cantidad_epocas_
        self._continuar = False
        self._juegos()

    def hay_suficientes(self):
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
        num = 0
        for juego in self.juegos:
            num = num + juego.celdas[i][j].estado
        return num

    def _cambiar(self, num):
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
        final = []
        for i in range(15):
            final.append([])
            for j in range(15):
                final[i].append(self._sumar(i, j))
                final[i][j] = self._cambiar(final[i][j])
        return final


def tablero_aleatorio():
    grilla = Grilla(7, 8)
    return grilla.grilla_final()
