from Funciones.funciones_palabras import palabra_es_valida


class Turno:
    """
    VARIABLES
    _letras: str → letras usadas en el turno (sin orden)
    _palabra: str → la palabra que se forma
    _casilleros_usados: set tuple → guarda las posiciones de los casilleros usados
    _letra_actual: str → guarda el valor de la letra actual
    _pos_actual: str → el último valor del atril presionado
    _atril_usadas: array int → las claves del atril usadas
    _orientacion: str → la orientación de la palabra
    _turno_usuario_: bool → True si es el turno del usuario

    MÉTODOS
    set_letra_actual: cambia el valor de _letra_actual
    get_letra_actual: devuelve el valor de letra actual → str
    set_pos_actual: cambia el valor de _pos_actual
    get_pos_actual: devuelve el valor de _pos_actual → str
    agregar_casillero: agrega la tupla mandada a _casilleros_usados
    sacar_casillero: saca la tupla mandada de _casilleros_usados
    get_casilleros_usados: devuelve lista de las tuplas → list tuple
    definir_palabra: arma la palabra a partir de las tuplas mandadas
    get_palabra: devuelve _palabra → str
    definir_puntos: calcula los puntos de la palabra y lo devuelve → int
    evaluar_palabra: se fija si la palabra es válida y los puntos, si el válida devuelve los puntos y si no devuelve 100 → int
    limpiar: resetea todos los valores menos el tiempo
    get_orientación: devuelve la orientacion → str
    set_letras: agrega la letra actual a _letras
    get_letras: devuelve _letras → str
    countdown: el contador empieza
    get_tiempo: devuelve _tiempo → int
    es_turno_usuario: devuelve True si es el turno del usuario → bool
    reinicio: reinicia todas las variables para el cambio de turno y cambia de un turno a otro
    fin → por ahora no hace nada
    """

    def __init__(self):
        self._letras = ""
        self._casilleros_usados = set()
        self._letra_actual = ""
        self._atril_usadas = []
        self._pos_actual = ""
        self._palabra = ""
        self._orientacion = ""
        self._turno_usuario = True
        self._lista_palabras = []
        self._puntaje = 0

    # Letra Actual
    def set_letra_actual(self, letra):
        self._letra_actual = letra

    def get_letra_actual(self):
        return self._letra_actual

    # Pos Actual
    def set_pos_actual(self, pos):
        self._pos_actual = pos

    def get_pos_actual(self):
        return self._pos_actual

    # Casilleros usados
    def agregar_casillero(self, pos):
        self._casilleros_usados.add(pos)
        if len(self._casilleros_usados) == 2:
            casilleros = list(self._casilleros_usados)
            print("los casilleros: ", casilleros[0][0], " ", casilleros[1][0])
            if casilleros[0][0] == casilleros[1][0]:
                self._orientacion = "horizontal"
            elif casilleros[0][1] == casilleros[1][1]:
                self._orientacion = "vertical"

    def sacar_casillero(self, pos):
        self._casilleros_usados.discard(pos)

    def get_casilleros_usados(self):
        return list(self._casilleros_usados)

    def set_casilleros_usados(self, c):
        self._casilleros_usados = c

    # PALABRA
    def definir_palabra(self, matriz):
        if self._orientacion == "horizontal":
            self._casilleros_usados = sorted(self._casilleros_usados, key=lambda tupla: tupla[1])
            # print("casilleros ordenados: ",self._casilleros_usados)
        elif self._orientacion == "vertical":
            self._casilleros_usados = sorted(self._casilleros_usados, key=lambda tupla: tupla[0])
        for pos in self._casilleros_usados:
            self._palabra = self._palabra + matriz[pos[0]][pos[1]].get_letra()

    def get_palabra(self):
        return self._palabra

    def set_palabra(self, p):
        self._palabra = p

    # EVALUAR PALABRA
    def definir_puntos(self, matriz, puntos):
        puntaje = 0
        for pos in self._casilleros_usados:
            puntaje = puntaje + matriz[pos[0]][pos[1]].devolver_puntos(puntos, self._palabra)
        self._puntaje = puntaje
        return puntaje

    # -- Cuando termina el turno evalua si la palabra es válida y devuelve el puntaje
    def evaluar_palabra(self, matriz, diccionario, nivel):
        self.definir_palabra(matriz)
        if palabra_es_valida(self._palabra, diccionario, nivel["palabras"]):
            print("La palabra es válida y es: ", self._palabra)
            return self.definir_puntos(matriz, nivel["puntos"])
        else:
            return 100

    # Limpiar Valores si se ingresa palabra no valida
    def limpiar(self):
        self._palabra = ""
        self._letras = ""
        self._atril_usadas = []
        self._letra_actual = ""
        self._orientacion = ""
        self._casilleros_usados.clear()
        self._casilleros_usados = set()

    # ORIENTACIÓN
    def get_orientacion(self):
        return self._orientacion

    # Letras
    def set_letras(self, letra):
        self._letras = self._letras + letra

    def get_letras(self):
        return self._letras

    # Usadas atril
    def add_atril_usada(self, num):
        self._atril_usadas.append(num)

    def get_atril_usadas(self):
        return self._atril_usadas

    # Turno
    def es_turno_usuario(self):
        return self._turno_usuario

    def set_turno_usuario(self, va):
        self._turno_usuario = va

    def set_puntaje(self,p):
        self._puntaje = p

    # Lista de palabras
    def add_lista_palabras(self, palabra, puntos):
        dato = palabra + ": " + str(puntos)
        self._lista_palabras.append(dato)

    def get_lista_palabras(self):
        datos = '\n'.join(self._lista_palabras)
        return datos

    # ReiniciarValores
    def reinicio(self):
        if len(self._palabra) > 0:
            self.add_lista_palabras(self._palabra, self._puntaje)
        self._palabra = ""
        self._letras = ""
        self._letra_actual = ""
        self._orientacion = ""
        self._casilleros_usados.clear()
        self._casilleros_usados = set()
        self._puntaje = 0
        if self._turno_usuario:
            self._turno_usuario = False
        else:
            self._turno_usuario = True

    # Fin de turno
    def fin(self):
        print("palabra: ", self._palabra)
