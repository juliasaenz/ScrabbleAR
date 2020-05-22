from Funciones_Matriz import ImprimirPalabra
from Funciones_Matriz import IniciarMatriz
from Funciones_Matriz import RecorrerMatriz

IniciarMatriz()

ImprimirPalabra()
print("¿quiere volver a cargar datos en la matriz?")
decision=input('ingrese "si" o "no"')
while (decision=="si"):
    ImprimirPalabra()   #importante aún no hice lo de las coliciones entre palabras 
    print("¿quiere volver a cargar datos en la matriz?")
    decision=input('ingrese "si" o "no"')
