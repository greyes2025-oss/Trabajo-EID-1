import tkinter as tk
from tkinter import messagebox, scrolledtext, font
import sympy as sp

# Importamos nuestros propios archivos.
import analisis
import grafica

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Funciones")
        self.root.geometry("700x600")

        # Fuentes
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)
        
        #Variables de estado
        self.funcion = None
        self.inter_x = []
        self.inter_y = None
        self.punto_evaluado = None

        # Contenedor principal
        main_frame = tk.Frame(root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sección de Entradas
        input_frame = tk.LabelFrame(main_frame, text="Entrada de Datos", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, text="Función f(x):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_funcion = tk.Entry(input_frame, width=40, font=("Helvetica", 12))
        self.entry_funcion.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Evaluar en x (opcional):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_valor_x = tk.Entry(input_frame, width=20, font=("Helvetica", 12))
        self.entry_valor_x.grid(row=1, column=1, sticky="w", padx=5)
        
        #Botones de Accion 
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.btn_analizar = tk.Button(button_frame, text="Analizar Función", command=self.analizar, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white")
        self.btn_analizar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.btn_graficar = tk.Button(button_frame, text="Generar Gráfico", command=self.graficar, font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", state=tk.DISABLED)
        self.btn_graficar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        #Sección de Resultados
        results_frame = tk.LabelFrame(main_frame, text="Resultados y Desarrollo Computacional", padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.texto_resultados = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=("Courier New", 11), state=tk.DISABLED)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True)

    def analizar(self):
        # Esta es la función que se ejecuta al apretar el botón analizar
        self.texto_resultados.config(state=tk.NORMAL)
        self.texto_resultados.delete(1.0, tk.END)
        self.btn_graficar.config(state=tk.DISABLED)
        self.punto_evaluado = None

        # Aquí le pasamos el texto a sympy para que lo convierta en una ecuación
        funcion_str = self.entry_funcion.get().strip()
        if not funcion_str:
            messagebox.showerror("Error", "El campo de la función no puede estar vacío.")
            return
        
        try:
            self.funcion = sp.sympify(funcion_str, locals={'x': sp.Symbol('x')})
        except (sp.SympifyError, SyntaxError):
            messagebox.showerror("Error de Sintaxis", f"La función '{funcion_str}' no es válida.\nUse la sintaxis de Python (ej: x**2 o sqrt(x)).")
            return
        
        self.escribir_titulo(f"Análisis de f(x) = {self.funcion}")

        # Aquí empieza a llamar a las funciones del cerebro analisis
        valor_x_str = self.entry_valor_x.get().strip()
        if valor_x_str:
            try:
                valor_x = float(valor_x_str)
                resultado, pasos = analisis.evaluar_punto(self.funcion, valor_x)
                self.escribir_seccion("Evaluación en un Punto", pasos)
                if resultado is not None:
                    self.punto_evaluado = (valor_x, resultado)
            except ValueError:
                messagebox.showerror("Error", "El valor de 'x' para evaluar debe ser un número.")
                return

        dominio, pasos_dominio = analisis.calcular_dominio(self.funcion)
        self.escribir_seccion(dominio, pasos_dominio)
        
        recorrido, pasos_recorrido = analisis.calcular_recorrido(self.funcion)
        self.escribir_seccion(recorrido, pasos_recorrido)
        
        self.inter_x, self.inter_y, pasos_inter = analisis.calcular_intersecciones(self.funcion)
        self.escribir_seccion("Cálculo de Intersecciones", pasos_inter)

        self.texto_resultados.config(state=tk.DISABLED)
        self.btn_graficar.config(state=tk.NORMAL)

    def graficar(self):
        # Cuando aprietan Generar Gráfico esta función llama al otro archivo
        # y le pasa toda la información que ya calculamos
        if self.funcion is None:
            messagebox.showwarning("Advertencia", "Primero debes analizar una función.")
            return
        grafica.generar_grafico(self.funcion, self.inter_x, self.inter_y, self.punto_evaluado)

    def escribir_titulo(self, titulo):
        self.texto_resultados.insert(tk.END, f"{'='*60}\n")
        self.texto_resultados.insert(tk.END, f"{titulo.center(60)}\n")
        self.texto_resultados.insert(tk.END, f"{'='*60}\n\n")

    def escribir_seccion(self, titulo, pasos):
        self.texto_resultados.insert(tk.END, f"-> {titulo}:\n")
        for paso in pasos:
            self.texto_resultados.insert(tk.END, f"   {paso}\n")
        self.texto_resultados.insert(tk.END, "\n")

# Este bloque hace que este archivo sea el que se ejecuta.
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()