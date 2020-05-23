class Casillero:
    '''Define un casillero del tablero.
        Propiedades:
            tipo: el tipo de casillero que es, por default en normal
            ocupada: un boolean que dice si el casillero está o no ocupado por una letra
            letra: el caracter que se encuentra en el casillero, por default vacio
            palabra: la palabra que corresponde a la letra del casillero, por default vacio'''

    #Constructor
    def __init__(self,tipo_):
        self.tipo = tipo_
        ocupada = False
        letra = None
        palabra = None

    #Métodos
    def ocupar_casillero (self,letra_):
        '''Cuando se ocupa un casillero guarda el valor y pasa a estar ocupada'''
        self.ocupada = True
        self.letra = letra_

    def guardar_palabra(self,palabra_):
        '''Guarda la palabra correspondiente al caracter del casillero'''
        self.palabra = palabra_

    def devolver_puntos(self,diccionario):
        '''Depende del tipo de casillero devuelve los puntos correspondientes'''
        if(self.tipo == "doble_letra"):
            return self.doble_letra(self,diccionario)
        elif (self.tipo == "triple_letra"):
            return self.triple_letra(self,diccionario)
        elif (self.tipo == "doble_palabra"):
            return self.doble_palabra(self,diccionario)
        elif (self.tipo == "triple_palabra"):
            return self.triple_palabra(self,diccionario)
        elif (self.tipo == "menos_uno"):
            return self.menos_uno(self,diccionario)
        elif (self.tipo == "menos_dos"):
            return self.menos_dos(self,diccionario)
        elif (self.tipo == "menos_tres"):
            return self.menos_tres()
        else:
            return diccionario[self.letra]

    def devolver_estado(self):
        if(self.ocupada):
            return self.letra
        else:
            return False

    #Casilleros Especiales
    def doble_letra(self,diccionario):
        ''' Devuelve el doble puntaje de la letra'''
        return diccionario[self.letra]*2

    def triple_letra(self, diccionario):
        ''' Devuelve el triple puntaje de la letra'''
        return diccionario[self.letra] * 3

    def doble_palabra(self,diccionario):
        ''' Devuelve el doble puntaje de la palabra'''
        puntos = 0
        for letra in self.palabra:
            puntos = puntos + diccionario[letra]
        return puntos*2

    def triple_palabra(self,diccionario):
        ''' Devuelve el triple puntaje de la palabra'''
        puntos = 0
        for letra in self.palabra:
            puntos = puntos + diccionario[letra]
        return puntos*3

    def menos_uno(self,diccionario):
        ''' Resta 1 a la letra'''
        return diccionario[self.letra] -1

    def menos_dos(self,diccionario):
        ''' Resta 2 a la letra'''
        return diccionario[self.letra] -2

    def menos_tres(self,diccionario):
        ''' Resta 3 a la letra'''
        return diccionario[self.letra] -3