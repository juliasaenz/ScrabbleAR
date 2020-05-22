
matriz=[] #no existen vectores en python (solo con libreria numpy x ej),por esto
          # hice la matriz con dos listas una dentro de otra
          
def IniciarMatriz(): #Inicia la matriz en None/tmb sirve para borrar todos los datos inregsados en la misma
    global matriz
    for z in range(15):
        matriz.append([])           
        for x in range(15):     
            matriz[z].append(None)

def RecorrerMatriz():#imprime toda la matriz 
    global matriz
    for x in range(15):
        for z in range(15):
            print(matriz[x][z], end=" ")
        print()

def Vertical_Arriba(palabra,base,altura): #carga los datos en su sentido, si sobrepasan el limite, carga hasta donde puede
    contador=0                            #informa que sobrepasa y borra los datos q cargo 
    if((altura+1)>=len(palabra)):               #Usa(RecorrerMatriz, para mostrar el progreso)
        while(contador<len(palabra)):
            matriz[altura][base]=palabra[contador]
            contador=contador+1
            altura=altura-1
    else:
        while((altura+1)!=0):
            matriz[altura][base]=palabra[contador]
            contador=contador+1
            altura=altura-1
        RecorrerMatriz()
        altura=(altura+contador)
        print()
        print("La palabra no entra en el tablero en la orientacion y ubicación que indicó")
        print()
        while((altura+1)!=0):
            matriz[altura][base]=None
            altura=altura-1
    RecorrerMatriz()
    
def Vertical_Abajo(palabra,base,altura):#carga los datos en su sentido, si sobrepasan el limite, carga hasta donde puede
    contador=0                          #informa que sobrepasa y borra los datos q cargo
    if((15-altura)>=len(palabra)):          #Usa(RecorrerMatriz, para mostrar el progreso)
        while(contador < len(palabra)):
            matriz[altura][base]=palabra[contador]
            contador=contador+1
            altura=altura+1
    else:
        while((15-altura)!=0):
            matriz[altura][base]=palabra[contador]
            contador=contador+1
            altura=altura+1

        RecorrerMatriz()
        altura=(altura-contador)
        print()
        print("La palabra no entra en el tablero en la orientacion y ubicación que indicó")
        print()
        while((15-altura)!=0):
            matriz[altura][base]=None
            altura=altura+1
    RecorrerMatriz()
        
def Horizontal(palabra,base,altura):    #carga los datos en su sentido, si sobrepasan el limite, carga hasta donde puede
    contador=0                          #informa que sobrepasa y borra los datos q cargo
    if((15-base)>=len(palabra)):            #Usa(RecorrerMatriz, para mostrar el progreso)
        while(contador<len(palabra)):
            matriz[altura][base]=palabra[contador]
            contador=contador+1
            base=base+1
    else:
        while((15-base)!=0):
            matriz[altura][base]=palabra[contador]
            contador=contador+1
            base=base+1
        RecorrerMatriz()
        base=(base-contador)
        print()
        print("La palabra no entra en el tablero en la orientacion y ubicación que indicó")
        print()
        while((15-base)!=0):
            matriz[altura][base]=None
            base=base+1
    RecorrerMatriz()


    
def ImprimirPalabra():              #carga en la matriz la cadena-de-caracteres que le digas, desde ,la ubicacion que le digas, en el sentido que le indiques 
    print("Ingrese una palabra")    #Usa las funciones(Horizontal y Verticales)
    palabra=input()
    while(7<=len(palabra)):
        print("la palabra no puede ser mas larga que 7")
        print("intente nuevamente")
        palabra=input()
    palabra=palabra.upper()

    print("ingrese las cordenadas x,y")
    print("desde estas empezara a crearse la palabra")
    print("tenga en cuenta que el tablero es 15 x 15")
    print("partiendo desde la posicion (0,0) hasta (14,14)")
    base=int(input("valor de x: ")) 
    altura=int(input("valor de y: "))
    
    print ('Ingrese la orientacion, esta puede ser:')
    print('"1"->Vertical Arriba')
    print('"2"->Vertical Abajo')
    print('"3"->Horizontal')

    orientacion=input()
    while((orientacion != "1")and(orientacion !="2")and(orientacion !="3")):
        print("numero erroneo, por favor")      
        print("ingrese alguna de las tres opciones")
        orientacion=input()

    if(orientacion=="1"):
           Vertical_Arriba(palabra,base,altura)
    elif(orientacion=="2"):
        Vertical_Abajo(palabra,base,altura)
    elif(orientacion=="3"):
        Horizontal(palabra,base,altura)


      

