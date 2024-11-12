import random
import copy
import time
import heapq
import tkinter as tk
from tkinter import messagebox

nodos_explorados = 0
camino = []

# Funciones
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

def obtener_candidatos(tablero, fila, col):
    candidatos = set(range(1, 10))
    for i in range(9):
        if tablero[fila][i] in candidatos:
            candidatos.discard(tablero[fila][i])
        if tablero[i][col] in candidatos:
            candidatos.discard(tablero[i][col])
    inicio_fila = fila - fila % 3
    inicio_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if tablero[inicio_fila + i][inicio_col + j] in candidatos:
                candidatos.discard(tablero[inicio_fila + i][inicio_col + j])
    return list(candidatos)

def encontrar_vacio_menos_candidatos(tablero):
    min_heap = []
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                candidatos = obtener_candidatos(tablero, i, j)
                heapq.heappush(min_heap, (len(candidatos), i, j, candidatos))
    return min_heap

def resolver_sudoku(tablero):
    global nodos_explorados
    global camino
    cola_prioridad = encontrar_vacio_menos_candidatos(tablero)
    if not cola_prioridad:
        return True
    _, fila, col, candidatos = heapq.heappop(cola_prioridad)

    for num in candidatos:
        if es_valido(tablero, fila, col, num):
            nodos_explorados += 1
            tablero[fila][col] = num
            camino.append([fila + 1, col + 1, num, nodos_explorados])
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

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Paso a Paso")
        self.tablero = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.dibujar_tablero()
        self.dibujar_botones()

    def dibujar_tablero(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for fila in range(9):
            for col in range(9):
                entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=fila, column=col, padx=5, pady=5, ipady=5)
                self.entries[fila][col] = entry

    def dibujar_botones(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text="Generar Fácil", command=lambda: self.generar_tablero('facil')).pack(side='left', padx=5)
        tk.Button(frame, text="Generar Medio", command=lambda: self.generar_tablero('medio')).pack(side='left', padx=5)
        tk.Button(frame, text="Generar Difícil", command=lambda: self.generar_tablero('dificil')).pack(side='left', padx=5)
        tk.Button(frame, text="Resolver Paso a Paso", command=self.resolver_paso_a_paso).pack(side='left', padx=5)
        tk.Button(frame, text="Limpiar", command=self.limpiar).pack(side='left', padx=5)

    def generar_tablero(self, dificultad):
        self.tablero = self._generar_tablero(dificultad)
        for fila in range(9):
            for col in range(9):
                if self.tablero[fila][col] != 0:
                    self.entries[fila][col].delete(0, tk.END)
                    self.entries[fila][col].insert(0, str(self.tablero[fila][col]))
                    self.entries[fila][col].config(state='disabled')
                else:
                    self.entries[fila][col].config(state='normal')
                    self.entries[fila][col].delete(0, tk.END)

    def _generar_tablero(self, dificultad):
        tablero = [[0 for _ in range(9)] for _ in range(9)]
        self._llenar_tablero(tablero)
        celdas_a_llenar = {
            'facil': random.randint(35, 50),
            'medio': random.randint(22, 34),
            'dificil': random.randint(10, 21)
        }[dificultad]
        self._quitar_numeros(tablero, celdas_a_llenar)
        return tablero

    def _llenar_tablero(self, tablero):
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    numeros = list(range(1, 10))
                    random.shuffle(numeros)
                    for num in numeros:
                        if es_valido(tablero, fila, col, num):
                            tablero[fila][col] = num
                            if self._llenar_tablero(tablero):
                                return True
                            tablero[fila][col] = 0
                    return False
        return True

    def _quitar_numeros(self, tablero, celdas_a_llenar):
        celdas_a_quitar = 81 - celdas_a_llenar
        while celdas_a_quitar > 0:
            fila, col = random.randint(0, 8), random.randint(0, 8)
            if tablero[fila][col] != 0:
                tablero[fila][col] = 0
                celdas_a_quitar -= 1

    def resolver_paso_a_paso(self):
        self.tablero = [[int(self.entries[fila][col].get()) if self.entries[fila][col].get().isdigit() else 0
                        for col in range(9)] for fila in range(9)]
        start_time = time.time()
        self.nodos_explorados = 0
        if self._resolver_paso_a_paso():
            elapsed_time = time.time() - start_time
            messagebox.showinfo("Sudoku", f"¡Resuelto! se revisaron {self.nodos_explorados} nodos en {round(elapsed_time, 3)} segundos")
        else:   
            messagebox.showerror("Error", "No se pudo resolver el Sudoku")

    def _resolver_paso_a_paso(self):
        cola_prioridad = encontrar_vacio_menos_candidatos(self.tablero)
        if not cola_prioridad:
            return True

        _, fila, col, candidatos = heapq.heappop(cola_prioridad)

        for num in candidatos:
            if es_valido(self.tablero, fila, col, num):
                self.tablero[fila][col] = num
                self.entries[fila][col].delete(0, tk.END)
                self.entries[fila][col].insert(0, str(num))
                self.entries[fila][col].update()
                time.sleep(0.01)
                self.nodos_explorados += 1

                if self._resolver_paso_a_paso():
                    return True

                self.tablero[fila][col] = 0
                self.entries[fila][col].delete(0, tk.END)
                self.entries[fila][col].update()
                time.sleep(0.1)

        return False

    def limpiar(self):
        for fila in range(9):
            for col in range(9):
                self.entries[fila][col].config(state='normal')
                self.entries[fila][col].delete(0, tk.END)
                self.tablero[fila][col] = 0
        global nodos_explorados
        global camino
        nodos_explorados = 0
        camino = []

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()