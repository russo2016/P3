import random

nodos_explorados = 0
camino = []
#funciones
def es_valido(tablero, fila, col, num):
    for i in range(9):
        if tablero[fila][i] == num:
            return False

    for i in range(9):
        if tablero[i][col] == num:
            return False

    inicio_fila = fila - fila % 3
    inicio_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if tablero[i + inicio_fila][j + inicio_col] == num:
                return False

    return True

def encontrar_vacio_menos_candidatos(tablero):
    min_candidatos = 10
    mejor_celda = None
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                candidatos = obtener_candidatos(tablero, i, j)
                if len(candidatos) < min_candidatos:
                    min_candidatos = len(candidatos)
                    mejor_celda = (i, j)
    return mejor_celda

def obtener_candidatos(tablero, fila, col):
    candidatos = set(range(1, 10))
    for i in range(9):
        candidatos.discard(tablero[fila][i])
        candidatos.discard(tablero[i][col])
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            candidatos.discard(tablero[inicio_fila + i][inicio_col + j])
    return list(candidatos)

def resolver_sudoku(tablero):
    vacio = encontrar_vacio_menos_candidatos(tablero)
    global nodos_explorados
    global camino
    if not vacio:
        return True
    fila, col = vacio

    for num in range(1, 10):
        if es_valido(tablero, fila, col, num):
            nodos_explorados += 1
            tablero[fila][col] = num
            camino.append([fila+1, col+1, num, nodos_explorados])

            if resolver_sudoku(tablero):
                return True
            else:
                tablero[fila][col] = 0
                camino.pop()
    return False

def llenar_tablero(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                numeros = list(range(1, 10))
                random.shuffle(numeros)
                for num in numeros:
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if llenar_tablero(tablero):
                            return True
                        tablero[fila][col] = 0
                return False
    return True

def quitar_numeros(tablero, celdas_a_llenar):
    celdas_a_quitar = 81 - celdas_a_llenar
    while celdas_a_quitar > 0:
        fila, col = random.randint(0, 8), random.randint(0, 8)
        if tablero[fila][col] != 0:
            tablero[fila][col] = 0
            celdas_a_quitar -= 1

def generar_tablero(dificultad):
    tablero = [[0 for i in range(9)] for i in range(9)]
    celdas_a_llenar = {
        'facil': random.randint(35, 50),
        'medio': random.randint(22, 34),
        'dificil': random.randint(10, 21)
    }.get(dificultad, 35)
    

    llenar_tablero(tablero)
    quitar_numeros(tablero, celdas_a_llenar)
    
    return tablero

def ingresar_tablero(dificultad):
    tablero = [[0 for i in range(9)] for i in range(9)]
    print("Ingresa el tablero de Sudoku manualmente:")
    celdas_a_llenar = {
        'facil': 50,
        'medio': 34,
        'dificil': 21
    }.get(dificultad, 50)
    i = 0
    while i < celdas_a_llenar:
        print("\nTablero actual:")
        for fila in tablero:
            print(fila)

        fila = int(input("Ingresa la fila (1-9) o -1 para finalizar: ")) - 1
        if fila == -2:
            break

        col = int(input("Ingresa la columna (1-9): ")) - 1
        num = int(input("Ingresa el número (1-9) o 0 para dejar vacío: "))

        if 0 <= fila < 9 and 0 <= col < 9 and 0 <= num <= 9:
            if num == 0 or es_valido(tablero, fila, col, num):
                if num != 0:
                    tablero[fila][col] = num
                    i+=1
                else:
                    tablero[fila][col] = num
            else:
                print("Número inválido. No se respetan las reglas del sudoku.")
        else:
            print("fila, colummna o numero invalido.")    
    return tablero

#main
print("Selecciona el tipo de tablero:")
print("1. Generar tablero aleatorio")
print("2. Ingresar tablero manualmente")
modo = input("Ingresa el número de la opción elegida: ")

if modo == '1':
    print("\nSelecciona la dificultad del Sudoku:")
    print("1. Fácil")
    print("2. Medio")
    print("3. Difícil")
    dificultad = input("Ingresa el número de la dificultad elegida: ")

    if dificultad == '1':
        tablero = generar_tablero('facil')
    elif dificultad == '2':
        tablero = generar_tablero('medio')
    elif dificultad == '3':
        tablero = generar_tablero('dificil')
    else:
        print("Dificultad no válida. Generando tablero fácil.")
        tablero = generar_tablero('facil')

elif modo == '2':
    print("\nSelecciona la dificultad del Sudoku:")
    print("1. Fácil")
    print("2. Medio")
    print("3. Difícil")
    dificultad = input("Ingresa el número de la dificultad elegida: ")
    if dificultad == '1':
        tablero = ingresar_tablero('facil')
    elif dificultad == '2':
        tablero = ingresar_tablero('medio')
    elif dificultad == '3':
        tablero = ingresar_tablero('dificil')
    else:
        print("Dificultad no válida. Generando tablero fácil.")
        tablero = generar_tablero('facil')
else:
    print("Opción no válida. Generando tablero fácil aleatorio.")
    tablero = generar_tablero('facil')

print("\nTablero inicial:")
for fila in tablero:
    print(fila)

nodos_explorados = 0
camino = []

print("\nResolución:")
if resolver_sudoku(tablero):
    for fila in tablero:
        print(fila)
else:
    print("No hubo solución")

print("Camino:")
i = 1
for paso in camino:
    print(f"numero {i} asentado: {paso[0],paso[1],paso[2]} en el nodo {paso[3]}")
    i+=1

print(f"Nodos explorados: {nodos_explorados}")

