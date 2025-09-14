import matplotlib.pyplot as plt
import sympy as sp

# Símbolo x para graficar
x_sym = sp.symbols('x')

def generar_grafico(funcion, inter_x, inter_y, punto_evaluado=None):
    func_numerica = sp.lambdify(x_sym, funcion, modules=['math'])    
    # Creamos puntos en el eje X
    x_vals = [i / 50.0 for i in range(-1000, 1001)]
    y_vals = []
    
    # Asintotas
    for val in x_vals:
        try:
            resultado = func_numerica(val)
            # Si el resultado es un número gigante es que estamos en una asíntota
            if abs(resultado) > 100:
                y_vals.append(None)
            else:
                y_vals.append(resultado)
        except Exception:
            y_vals.append(None)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 8))
    ax = plt.gca()

    # Esto es para que los ejes se vean 
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # ax.plot dibuja la línea de la función. zorder=1 la pone al fondo.
    ax.plot(x_vals, y_vals, label=f'f(x) = {funcion}', zorder=1)

    # ax.scatter dibuja los puntitos. zorder=5 los pone por encima de todo.
    if inter_x:
        ax.scatter(inter_x, [0]*len(inter_x), color='green', s=60, zorder=5, label='Intersecciones Eje X')

    if inter_y is not None:
        ax.scatter(0, inter_y, color='purple', s=60, zorder=5, label='Intersección Eje Y')
        
    if punto_evaluado:
        px, py = punto_evaluado
        ax.scatter(px, py, color='red', s=100, zorder=5, ec='black', label=f'Punto Evaluado ({px}, {py})')

    # Configuración del gráfico
    plt.title("Análisis Gráfico de la Función", fontsize=16)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("f(x)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6) #
    plt.legend() # Muestra las etiquetas de los colores.
    
    # Ajustar límites visuales para una mejor presentación
    y_validos = [y for y in y_vals if y is not None]
    if y_validos:
        min_y, max_y = min(y_validos), max(y_validos)
        padding = (max_y - min_y) * 0.1
        plt.ylim(min_y - padding -1, max_y + padding + 1)

    # Abre la ventana que muestra el gráfico.
    plt.show()