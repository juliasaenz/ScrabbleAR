import PySimpleGUI as sg
import estilo
class Casillero:
    '''Define un casillero del tablero.
        Propiedades:
            tipo: el tipo de casillero que es, por default en normal
            ocupada: un boolean que dice si el casillero está o no ocupado por una letra
            letra: el caracter que se encuentra en el casillero, por default vacio
            palabra: la palabra que corresponde a la letra del casillero, por default vacio'''

    #Constructor
    def __init__(self,tipo_):
        self._tipo = tipo_
        self._ocupada = False
        self._letra = " "
        self._palabra = ""

    #Métodos
    def ocupar_casillero (self,letra_):
        '''Cuando se ocupa un casillero guarda el valor y pasa a estar ocupada'''
        self._ocupada = True
        self._letra = letra_
        if(letra_ == ""):
           self.vaciar_casillero()

    def vaciar_casillero (self):
        '''Cuando se ocupa un casillero guarda el valor y pasa a estar ocupada'''
        self._ocupada = False
        self._letra = ""

    def esta_vacia(self):
        return self._ocupada

    def set_palabra(self,palabra_):
        '''Guarda la palabra correspondiente al caracter del casillero'''
        self._palabra = palabra_

    def get_palabra(self):
        return self._palabra

    def devolver_puntos(self,puntos,palabra_):
        '''Depende del tipo de casillero devuelve los puntos correspondientes'''
        self.set_palabra(palabra_)
        if(self._tipo == "doble_letra"):
            return self.doble_letra(self,puntos)
        elif (self._tipo == "triple_letra"):
            return self.triple_letra(self,puntos)
        elif (self._tipo == "doble_palabra"):
            return self.doble_palabra(self,puntos)
        elif (self._tipo == "triple_palabra"):
            return self.triple_palabra(self,puntos)
        elif (self._tipo == "menos_uno"):
            return self.menos_uno(self,puntos)
        elif (self._tipo == "menos_dos"):
            return self.menos_dos(self,puntos)
        elif (self._tipo == "menos_tres"):
            return self.menos_tres()
        else:
            return puntos[self._letra]

    def devolver_estado(self):
        if(self._ocupada):
            return self._letra
        else:
            return ' '

    def dibujar(self,clave):
        return sg.Button(self._letra, **estilo.bt,key=clave, disabled=True)

    #Casilleros Especiales
    def doble_letra(self,puntos):
        ''' Devuelve el doble puntaje de la letra'''
        return puntos[self._letra]*2

    def triple_letra(self, puntos):
        ''' Devuelve el triple puntaje de la letra'''
        return puntos[self._letra] * 3

    def doble_palabra(self,puntos):
        ''' Devuelve el doble puntaje de la palabra'''
        puntaje = 0
        for letra in self._palabra:
            puntaje = puntaje + puntos[letra]
        return puntaje*2

    def triple_palabra(self,puntos):
        ''' Devuelve el triple puntaje de la palabra'''
        puntaje = 0
        for letra in self._palabra:
            puntaje = puntaje + puntos[letra]
        return puntaje*3

    def menos_uno(self,puntos):
        ''' Resta 1 a la letra'''
        return puntos[self._letra] -1

    def menos_dos(self,puntos):
        ''' Resta 2 a la letra'''
        return puntos[self._letra] -2

    def menos_tres(self,puntos):
        ''' Resta 3 a la letra'''
        return puntos[self._letra] -3