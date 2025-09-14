import sympy as sp
from sympy.solvers.inequalities import solve_univariate_inequality

# Definimos x como el símbolo
x = sp.symbols('x')

def evaluar_punto(funcion, valor_x):
    #Evalúa la función en un punto x, mostrando un paso a paso detallado.
    pasos = [f"1. Se solicita evaluar la función f(x) en x = {valor_x}."]
    try:
        # .subs() se encarga de reemplazar la x por el número que le pasamos.
        funcion_sustituida = funcion.subs(x, valor_x)
        pasos.append(f"2. Se sustituye x por {valor_x} en la función: f({valor_x}) = {funcion_sustituida}")

        # .evalf() calcula el resultado final en decimales
        resultado_eval = funcion_sustituida.evalf()
        resultado_redondeado = round(float(resultado_eval), 4)
        pasos.append(f"3. Se calcula el valor: f({valor_x}) = {resultado_redondeado}")
        pasos.append(f"4. El par ordenado resultante es ({valor_x}, {resultado_redondeado}).")
        
        return resultado_redondeado, pasos
        
    except Exception as e:
        pasos.append(f"Error: No se pudo evaluar el punto. El valor podría estar fuera del dominio. ({e})")
        return None, pasos

def calcular_dominio(funcion):

    pasos = ["Para encontrar el dominio, se buscan valores de 'x' que generen indefiniciones."]
    # Un set es como una lista pero no permite elementos repetidos
    restricciones = set()
    condiciones = []

    #Análisis de Denominadores 
    denominador = sp.denom(funcion)
    if denominador != 1:
        pasos.append(f"1. Se analiza el denominador: {denominador}. No puede ser cero.")
        try:
            # sp.solve() resuelve las ecuaciones
            soluciones = sp.solve(denominador, x)
            if soluciones:
                pasos.append(f"   Se resuelve {denominador} = 0, encontrando x = {soluciones}. Estos valores se excluyen.")
                for sol in soluciones:
                    restricciones.add(f"x ≠ {sol}")
            else:
                pasos.append("   El denominador nunca es cero. No hay restricciones por esta vía.")
        except Exception:
            pasos.append("   No se pudo resolver la ecuación del denominador.")

    #Análisis de Raíces Cuadradas (CORREGIDO)
    # Esto busca potencias elevadas a 1/2 (o 0.5), que es lo mismo que una raíz cuadrada
    raices = funcion.atoms(sp.Pow)
    for raiz in raices:
        if raiz.exp == 0.5 or raiz.exp == sp.Rational(1, 2):
            argumento = raiz.base
            pasos.append(f"2. Se analiza la raíz cuadrada con argumento: {argumento}. Su argumento debe ser >= 0.")
            try:
                # Esta función de sympy es la que resuelve inecuaciones como x - 4 >= 0
                sol_inecuacion = solve_univariate_inequality(argumento >= 0, x, relational=False)
                pasos.append(f"   Se resuelve la inecuación {argumento} >= 0, resultando en: {sol_inecuacion}.")
                condiciones.append(str(sol_inecuacion))
            except Exception:
                pasos.append(f"   No se pudo resolver la inecuación. La condición manual es {argumento} >= 0.")
                condiciones.append(f"{argumento} >= 0")
    
    #Construcción del resultado final
    dominio_str = "Dominio: Todos los números reales (ℝ)"
    partes_finales = []
    if restricciones:
        partes_finales.append(f"excepto {{{', '.join(sorted(list(restricciones)))}}}")
    if condiciones:
        partes_finales.append(f"cumpliendo que {' y '.join(condiciones)}")

    if partes_finales:
        dominio_str += " " + " ".join(partes_finales)

    return dominio_str, pasos

def calcular_intersecciones(funcion):
    pasos = []
    
    pasos.append("Intersección con el Eje Y (x=0)")
    try:
        inter_y_valor = funcion.subs(x, 0).evalf()
        inter_y = round(float(inter_y_valor), 4)
        pasos.append(f"Se evalúa f(0), resultando en {inter_y}. El punto es (0, {inter_y}).")
    except Exception:
        inter_y = None
        pasos.append("La función no está definida en x=0, no cruza el eje Y.")
        
    pasos.append("Intersecciones con el Eje X (y=0) ")
    pasos.append(f"Se iguala la función a cero: {funcion} = 0.")
    try:
        soluciones_x = sp.solve(funcion, x)
        inter_x = [round(float(s.evalf()), 4) for s in soluciones_x if s.is_real]
        
        if inter_x:
            pasos.append(f"Las soluciones reales encontradas son: {inter_x}.")
        else:
            pasos.append("No se encontraron soluciones reales. La función no cruza el eje X")
    except Exception:
        inter_x = []
        pasos.append("No se pudo resolver la ecuación f(x)=0.")
        
    return inter_x, inter_y, pasos

def calcular_recorrido(funcion):
    
    #Estima el recorrido. El cálculo analítico es complejo y no siempre es posible.
    pasos = ["El cálculo del recorrido es complejo. Se intentará un análisis para casos comunes."]
    
    if funcion.is_polynomial() and sp.degree(funcion, x) == 1:
        pasos.append("La función es una línea recta con pendiente, por lo que su recorrido son todos los reales.")
        return "Recorrido: Todos los números reales (ℝ)", pasos

    if funcion.is_polynomial() and sp.degree(funcion, x) == 2:
        # Calculo del vertice de una parabola
        a = funcion.coeff(x, 2)
        b = funcion.coeff(x, 1)
        vertice_x = -b / (2*a)
        vertice_y = funcion.subs(x, vertice_x).evalf()
        pasos.append(f"La función es una parábola. Su extremo está en el vértice y = {round(float(vertice_y), 4)}.")
        if a > 0: # Parábola abre hacia arriba
            return f"Recorrido: [{round(float(vertice_y), 4)}, ∞)", pasos
        else: # Parábola abre hacia abajo
            return f"Recorrido: (-∞, {round(float(vertice_y), 4)}]", pasos
    
    pasos.append("No se pudo determinar el recorrido con un método analítico simple.")
    return "Recorrido: No determinado analíticamente.", pasos