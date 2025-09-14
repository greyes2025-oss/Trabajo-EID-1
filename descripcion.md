# Analizador de Funciones 
### Integrantes
* Bastian Liempi
* Martin Hernandez
* Cristoper Parra
* Gerlac Reyes

---

## Descripción del Proyecto

Este proyecto es una aplicación de escritorio desarrollada en Python que funciona como un **analizador de funciones matemáticas**. La herramienta permite al usuario ingresar una función, analizar sus propiedades fundamentales y visualizarla gráficamente.

El programa destaca por exponer el **desarrollo computacional detallado** para justificar cada resultado, cumpliendo con los requisitos del curso de Álgebra para la Computación.

---

## Características Principales

* **Análisis Detallado**: Calcula y justifica el proceso para obtener:
    * **Dominio**: Identifica restricciones en funciones racionales y raíces cuadradas.
    * **Recorrido**: Analiza casos comunes como líneas y parábolas.
    * **Intersecciones con los ejes**: Muestra el cálculo para los puntos de corte.
* **Evaluación de Puntos**: Muestra un paso a paso de la sustitución y cálculo de `f(x)` para un valor `x` dado.
* **Visualización Profesional**: Genera un gráfico claro usando `matplotlib`, resaltando la función, sus intersecciones y el punto evaluado.
* **Estructura Modular**: El código está organizado en módulos que separan la lógica matemática de la interfaz gráfica.

---

## Estructura del Proyecto

El proyecto se compone de los siguientes módulos:

* `interfaz.py`: Archivo principal que construye la GUI y ejecuta la aplicación.
* `analisis.py`: Contiene toda la lógica matemática para el análisis de funciones.
* `grafica.py`: Se encarga de generar y mostrar el gráfico de la función.

---

## Tecnologías Utilizadas

* **Python 3**
* **Tkinter** para la GUI.
* **SymPy** para el manejo simbólico y análisis matemático.
* **Matplotlib** para la generación de gráficos.

---

## ¿Cómo Ejecutar el Proyecto?

1.  **Requisitos**: Asegúrate de tener Python 3 instalado. Luego, instala las librerías necesarias:
    ```bash
    pip3 install sympy matplotlib
    ```

2.  **Ejecución**: Coloca los tres archivos (`interfaz.py`, `analisis.py`, `grafica.py`) en la misma carpeta y ejecuta 