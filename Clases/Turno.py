from Funciones.funciones_palabras import palabra_es_valida
class Turno:

    def __init__(self,atril_):
        self._casilleros_usados = set()
        self._palabra = ""
        self._letra_actual = ""
        self._atril = atril_.copy()

    def get_casilleros_usdos(self):
        return self._casilleros_usados

    def get_jugador(self):
        return self._jugador

    def get_palabra(self):
        return self._palabra

    def get_letra_actual(self):
        return self._letra_actual

    def get_atril(self):
        return self._atril

    def set_letra_actual(self,letra):
        self._letra_actual = letra

    def set_palabra(self,matriz,direccion):
        if(direccion == "h"):
            self._casilleros_usados = sorted(self._casilleros_usados,key=lambda tupla: tupla[1])
            #print("casilleros ordenados: ",self._casilleros_usados)
        for pos in self._casilleros_usados:
            self._palabra = self._palabra + matriz[pos[0]][pos[1]].get_letra()

    #
    def agregar_casillero(self,pos):
        self._casilleros_usados.add(pos)
        #print("casilleros usados: ",self._casilleros_usados)

    def sacar_casillero(self,pos):
        self._casilleros_usados.remove(pos)
        #print("casilleros usados: ",self._casilleros_usados)

    def fin_turno(self,matriz,puntos,direccion):
        puntaje = 0
        self.set_palabra(matriz,direccion)
        for pos in self._casilleros_usados:
            puntaje = puntaje + matriz[pos[0]][pos[1]].devolver_puntos(puntos,self._palabra)
        self._letra_actual = ""
        self._casilleros_usados.clear()
        print("puntaje: ", puntaje)
        return puntaje
