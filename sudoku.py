import tkinter as tk
from tkinter import messagebox
import random
import time

def es_valido(tablero, fila, col, num):
    for i in range(9):
        if tablero[fila][i] == num or tablero[i][col] == num:
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

def verificar_unidad(unidad):
    if 0 in unidad:
        return False
    unidad = [num for num in unidad if num != 0 ]
    return len(unidad) == len(set(unidad)) and all(1 <= num <= 9 for num in unidad)


def verificar_solucion_(tablero):
    for fila in range(9):
        if not verificar_unidad([tablero[fila][col] for col in range(9)]):
            return False

    for col in range(9):
        if not verificar_unidad([tablero[fila][col] for fila in range(9)]):
            return False

    for inicio_fila in range(0, 9, 3):
        for inicio_col in range(0, 9, 3):
            if not verificar_unidad([tablero[fila][col] for fila in range(inicio_fila, inicio_fila + 3) for col in range(inicio_col, inicio_col + 3)]):
                return False

    return True

def es_tablero_valido(tablero):
    # Verificar conflictos en las celdas con valores iniciales
    for fila in range(9):
        for col in range(9):
            num = tablero[fila][col]
            if num != 0:
                # Temporalmente vaciamos la celda actual para verificar si el número es válido
                tablero[fila][col] = 0
                if not es_valido(tablero, fila, col, num):
                    # Restauramos el valor antes de salir
                    tablero[fila][col] = num
                    return False
                # Restauramos el valor después de la verificación
                tablero[fila][col] = num

    # Verificar que todas las celdas vacías tengan al menos un candidato posible
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                # Obtener los candidatos posibles
                candidatos = [num for num in range(1, 10) if es_valido(tablero, fila, col, num)]
                if not candidatos:  # Si no hay candidatos, el tablero es irresoluble
                    return False

    # Si no hay conflictos y todas las celdas vacías tienen candidatos, el tablero es válido
    return True

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
        tk.Button(frame, text="Generar Fácil", command=lambda: (self.limpiar(), self.generar_tablero('facil'))).pack(side='left', padx=5)
        tk.Button(frame, text="Generar Medio", command=lambda: (self.limpiar(), self.generar_tablero('medio'))).pack(side='left', padx=5)
        tk.Button(frame, text="Generar Difícil", command=lambda: (self.limpiar(), self.generar_tablero('dificil'))).pack(side='left', padx=5)
        tk.Button(frame, text="Resolver Paso a Paso", command=self.resolver_paso_a_paso).pack(side='left', padx=5)
        tk.Button(frame, text="Limpiar", command=self.limpiar).pack(side='left', padx=5)
        tk.Button(frame, text="Verificar Solución", command=self.verificar_solucion).pack(side='left', padx=5)


    def verificar_solucion(self):
        self.tablero = [[int(self.entries[fila][col].get()) if self.entries[fila][col].get().isdigit() else 0
                         for col in range(9)] for fila in range(9)]
        if verificar_solucion_(self.tablero):
            messagebox.showinfo("Sudoku", "¡Solución correcta!")
        else:
            messagebox.showerror("Error", "¡Solución incorrecta!")

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
        # Copia los valores del tablero actual desde las entradas y bloquea las celdas iniciales
        for fila in range(9):
            for col in range(9):
                valor = self.entries[fila][col].get()
                if valor.isdigit() and int(valor) != 0:
                    self.tablero[fila][col] = int(valor)
                    self.entries[fila][col].config(state='disabled')
                else:
                    self.tablero[fila][col] = 0

        # Verifica si el tablero inicial es válido antes de intentar resolverlo
        if not es_tablero_valido(self.tablero):
            messagebox.showerror("Error", "El tablero inicial tiene conflictos o es irresoluble.")
            return

        # Procede a resolver si el tablero es válido
        start_time = time.time()
        self.nodos_explorados = 0
        if self._resolver_paso_a_paso():
            elapsed_time = time.time() - start_time
            messagebox.showinfo("Sudoku",
                                f"¡Resuelto! se revisaron {self.nodos_explorados} nodos en {round(elapsed_time, 3)} segundos")
        else:
            messagebox.showerror("Error", "No se pudo resolver el Sudoku")

    def _resolver_paso_a_paso(self):
        vacio = encontrar_vacio(self.tablero)
        if not vacio:
            return True

        fila, col = vacio
        for num in range(1, 10):
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
                time.sleep(0.01)

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
