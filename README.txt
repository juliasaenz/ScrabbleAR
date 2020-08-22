ScrabbleAR

Este juego es el trabajo final de la materia Seminario de Python de la Facultad de Informatica de la UNLP, cursada en 2020

Alumna: Saenz Julia
Grupo: 28

Instalación y uso:
- Descargar el repositorio
- Ejecutar el archivo "ScrabbleAR.py"
- PySimpleGUI versión 4.19.0
- Pattern versión 3.6
- Python versión 3.6

*Las imágenes fueron diseñadas en Figma por Julia Saenz para este trabajo

------- INSTRUCCIONES --------

El juego se basa en las reglas del Scrabble tradicional: ambos jugadores deben utilizar letras, cada una con un puntaje, de una bolsa (en este caso un arreglo de fichas) para formar palabras y ubicarlas en un tablero con el fin de sumar puntos.
    A cada jugador se le dan al azar 7 letras de la bolsa y se elige uno de los dos para comenzar la partida. En el primer turno una de las fichas debe ser colocada en el casillero del medio, y en cualquier otro turno las palabras pueden ser ubicadas en cualquier parte del tablero.
    Las fichas pueden disponerse de forma horizontal o vertical y cuando se tenga la palabra se debe presionar el botón de “Terminar Turno”.Si la palabra ingresada es válida se sumarán los puntos acumulados y se pasará al turno del otro jugador; en caso de no serlo, se sacarán las fichas ingresadas del tablero y se le permitirá intentar otra combinación de fichas.
    El tablero cuenta con casilleros especiales que cambian el puntaje de una ficha o palabra. Estos casilleros especiales son:
Doble Letra: duplica el valor de la ficha en ese casillero
Triple Letra: triplica el calor de la ficha en ese casillero
Doble Palabra: duplica el valor de toda la palabra
Triple Palabra: triplica el valor de toda la palabra
Menos Uno: resta 1 punto a la ficha en ese casillero
Menos Dos: resta 2 puntos a la ficha en ese casillero
Menos Tres: resta 3 puntos a la ficha en ese casillero

    El juego termina cuando se acaba el tiempo o cuando se terminan las fichas de la bolsa. Se restan los puntos correspondientes a las fichas que siguen en el atril y el ganador es aquel que haya acumulado más puntos. En caso de que el puntaje sea uno de los 10 mejores, tendrá la opción de guardarlo en el “Top 10”.
    En cualquier momento de la partida puede decidir “Guardar Partida” lo que cerrará y guardará esa partida, que luego puede ser retomada eligiendo “Continuar” en el inicio. Solo se guardará la última partida, por lo que si sobreescribe un juego, no podrá recuperarlo.

En el Inicio y a lo largo de la partida es posible configurar la dificultad del juego, ya sea con los niveles Fácil, Medio o Difícil predeterminados, o combinando su propio nivel customizado. El nivel varía:
La dificultad de la Computadora
La cantidad de fichas en la bolsa
El puntaje de cada ficha
El tablero
El tiempo de juego
Los tipos de palabras válidos

Cada nivel tiene esta configuración:

Fácil
- Dificultad computadora: elige la mejor palabra de máximo 5 letras y la posiciona en un lugar aleatorio del tablero
- Cantidad de fichas:
    a, e: 12
    o: 9
    i, s: 6
    u, n, d, r: 5
    l, c: 4
    b, m, p, g, h, : 2,
    f, v, j, k, ñ, q, t, w, x, y, z: 1
- Puntos fichas:
    a, e, i, o, u, s, n, l, r, t: 1
    d, g: 2
    c, m, b, p: 3
    f, h, v, y: 4
    j: 6
    k, ñ, z: 8
    q, w, x: 10
- Tablero:
    doble letra: 20
    triple letra: 11
    doble palabra: 16
    triple palabra: 4
    menos uno: 16
    menos dos: 8
    menos tres: 0
- Tiempo: 3 minutos
- Tipos de palabras admitidas: sustantivos, adjetivos y verbos

Medio
- Dificultad computadora: elige la mejor palabra y la posiciona en un lugar aleatorio del tablero
- Cantidad de fichas:
    a, e: 11
    o: 8
    s: 7
    i: 6
    u, n, r: 5
    d, l, c, t: 4
    b, m, g, h, : 3
    p, g, h: 2
    f, v, j, k, ñ, q, t, w, x, y, z: 1
- Puntos fichas:
    a, e, i, o, u, s, n, l, r, t, c, d, g: 1
    m, b, p: 2
    f, h, v, y: 3
    j: 5
    k, ñ, z: 6
    q, w, x: 8
- Tablero:
    doble letra: 20
    triple letra: 16
    doble palabra: 4
    triple palabra: 4
    menos uno: 16
    menos dos: 8
    menos tres: 8
- Tiempo: 2 minutos
- Tipos de palabras admitidas: adjetivos y verbos

Difícil
- Dificultad computadora: elige la mejor palabra de máximo 5 letras y la posiciona en el lugar que le de más puntos
- Cantidad de fichas:
    a, e: 11
    o: 8
    s: 7
    i, u: 6
    n, r: 5
    d, l, c, t: 4
    b, m: 3
    p, g, h: 2
    f, v, j, k, ñ, q, w, x, y, z: 1
- Puntos fichas:
    a, e, i, o, u, s: 0
    n, l, r, t, c, d, g: 1
    m, b, p: 2
    f, h, v, y: 3
    j: 5
    k, ñ, z: 6
    q, w, x: 8
- Tablero:
    doble letra: 16
    triple letra: 4
    doble palabra: 12
    triple palabra: 4
    menos uno: 12
    menos dos: 16
    menos tres: 16
- Tiempo: 1 minuto
- Tipos de palabras admitidas: adjetivos y verbos
