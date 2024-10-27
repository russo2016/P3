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

def encontrar_vacio(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                return fila, col
    return None

def resolver_sudoku(tablero):
    vacio = encontrar_vacio(tablero)
    if not vacio:
        return True
    fila, col = vacio

    for num in range(1, 10):
        if es_valido(tablero, fila, col, num):
            tablero[fila][col] = num

            if resolver_sudoku(tablero):
                return True
            else:
                tablero[fila][col] = 0
    return False

tablero = [
    [0, 0, 0, 0, 7, 0, 0, 3, 8],
    [6, 0, 0, 0, 0, 5, 0, 0, 4],
    [0, 0, 0, 0, 3, 0, 1, 0, 0],
    [0, 2, 0, 7, 0, 0, 0, 0, 0],
    [5, 0, 3, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 2, 0, 7, 0],
    [0, 0, 6, 0, 4, 0, 0, 0, 0],
    [1, 0, 0, 9, 0, 0, 0, 0, 3],
    [8, 9, 0, 0, 1, 0, 0, 0, 0]
]

if resolver_sudoku(tablero):
    for fila in tablero:
        print(fila)
else:
    print("No hubo solución")
