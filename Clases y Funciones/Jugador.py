class Jugador:
    '''' bolsa de fichas, empieza en 60'''
    bolsa = 60

    def __init__(self, nom):
        self._puntaje = 0
        self._nombre = nom

    #setters y getters
    def set_nombre(self,nom):
        self._nombre = nom

    def set_puntaje(self,puntos):
        self._puntaje = puntos

    def get_nombre(self):
        return self._nombre

    def get_puntaje(self):
        return self._puntaje