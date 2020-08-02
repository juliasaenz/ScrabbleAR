""" Trabajo para Seminario de Python 2020 - Alumna Saenz Julia """

import PySimpleGUI as sg
import estilo


class Casillero:
    """
    VARIABLES DE INTANCIA

    _tipo: str → el tipo de casillero que es
    _bloqueada: bool → si el casillero se usó en otro turno es True
    _letra: str → La letra que lo ocupa

    MÉTODOS

    set_letra: cambia el valor de letra
    get_letra: devuelve el valor de la letra → str
    get_tipo:devuelve el tipo del casillero → str
    bloquear: variable bloquear se vuelve true
    esta_bloqueado: devuelve si está bloqueado → bool
    devolver_puntos: devuelve los puntos del casillero → int
        doble_letra → int
        triple_letra → int
        doble_palabra → int
        triple_palabra → int
        menos_uno → int
        menos_dos → int
        menos_tres → int
    dibujar → dibuja el botón → sg.Button
    """

    def __init__(self, tipo_="normal"):
        self._tipo = tipo_
        self._letra = ""
        self._bloqueado = False

    # Dibujar
    def dibujar(self, clave):
        if self._tipo == "doble_letra":
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#75E540"), border_width=0)
        elif self._tipo == "triple_letra":
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#E5CB40"), border_width=0)
        elif self._tipo == "doble_palabra":
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#E59940"), border_width=0)
        elif self._tipo == "triple_palabra":
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#E54040"), border_width=0)
        elif self._tipo == "menos_uno":
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#40E5E5"), border_width=0)
        elif self._tipo == "menos_dos":
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#4078E5"), border_width=0)
        elif self._tipo == "menos_tres":
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#E540DE"), border_width=0)
        else:
            return sg.Button(self._letra, key=clave, **estilo.bt, button_color=("black", "#FAFAFA"), border_width=0)

    # Tipo
    def get_tipo(self):
        return self._tipo

    def set_tipo(self, tip):
        self._tipo = tip

    # Bloquear
    def bloquear(self):
        self._bloqueado = True

    def esta_bloqueado(self):
        return self._bloqueado

    # Letra
    def set_letra(self, letra):
        self._letra = letra

    def get_letra(self):
        return self._letra

    # Casilleros Especiales
    def doble_letra(self, puntos):
        """ Devuelve el doble puntaje de la letra"""
        return puntos[self._letra] * 2

    def triple_letra(self, puntos):
        """ Devuelve el triple puntaje de la letra"""
        return puntos[self._letra] * 3

    def doble_palabra(self, puntos, pal):
        """ Devuelve el doble puntaje de la palabra"""
        puntaje = 0
        for letra in pal:
            puntaje = puntaje + puntos[letra]
        return puntaje * 2

    def triple_palabra(self, puntos, pal):
        """ Devuelve el triple puntaje de la palabra"""
        puntaje = 0
        for letra in pal:
            puntaje = puntaje + puntos[letra]
        return puntaje * 3

    def menos_uno(self, puntos):
        """ Resta 1 a la letra"""
        return puntos[self._letra] - 1

    def menos_dos(self, puntos):
        """ Resta 2 a la letra"""
        return puntos[self._letra] - 2

    def menos_tres(self, puntos):
        """ Resta 3 a la letra"""
        return puntos[self._letra] - 3

    # Puntos
    def devolver_puntos(self, puntos, palabra_):
        """Depende del tipo de casillero devuelve los puntos correspondientes"""
        if self._tipo == "doble_letra":
            return self.doble_letra(puntos)
        elif self._tipo == "triple_letra":
            return self.triple_letra(puntos)
        elif self._tipo == "doble_palabra":
            return self.doble_palabra(puntos, palabra_)
        elif self._tipo == "triple_palabra":
            return self.triple_palabra(puntos, palabra_)
        elif self._tipo == "menos_uno":
            return self.menos_uno(puntos)
        elif self._tipo == "menos_dos":
            return self.menos_dos(puntos)
        elif self._tipo == "menos_tres":
            return self.menos_tres(puntos)
        else:
            return puntos[self._letra]
