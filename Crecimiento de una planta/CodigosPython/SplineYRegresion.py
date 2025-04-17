import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.interpolate import CubicSpline
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para procesar los datos e interpolar
def procesar_datos():
    try:
        # Obtener los valores de X y Y del usuario
        dias_rosal = np.array([float(x) for x in entry_x.get().split(',')])
        alturas_rosal = np.array([float(y) if y != 'nan' else np.nan for y in entry_y.get().split(',')])

        # Datos de días faltantes (interpolación)
        dias_faltantes_rosal = dias_rosal[np.isnan(alturas_rosal)]

        # Coordenadas de los datos conocidos
        dias_conocidos_rosal = dias_rosal[~np.isnan(alturas_rosal)]
        alturas_conocidas_rosal = alturas_rosal[~np.isnan(alturas_rosal)]

        # 1. Interpolación Spline para Rosal
        interp_spline_rosal = CubicSpline(dias_conocidos_rosal, alturas_conocidas_rosal)
        alturas_faltantes_spline_rosal = interp_spline_rosal(dias_faltantes_rosal)

        # 2. Regresión Lineal para Rosal
        modelo_regresion_rosal = LinearRegression()
        modelo_regresion_rosal.fit(dias_conocidos_rosal.reshape(-1, 1), alturas_conocidas_rosal)
        alturas_faltantes_regresion_rosal = modelo_regresion_rosal.predict(dias_faltantes_rosal.reshape(-1, 1))

        # Mostrar los resultados finales
        result_text.set(f"Alturas faltantes (Spline): {alturas_faltantes_spline_rosal}\n"
                        f"Alturas faltantes (Regresión): {alturas_faltantes_regresion_rosal}")

        # Graficar los resultados
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(dias_conocidos_rosal, alturas_conocidas_rosal, 'o', label="Datos conocidos Rosal")
        ax.plot(dias_faltantes_rosal, alturas_faltantes_spline_rosal, 'd', label="Interpolación Spline Rosal")
        ax.plot(dias_faltantes_rosal, alturas_faltantes_regresion_rosal, '+', label="Regresión Lineal Rosal")
        ax.set_title("Crecimiento de la planta (Interpolación y Regresión Lineal)")
        ax.set_xlabel("Días")
        ax.set_ylabel("Altura (cm)")
        ax.legend()

        # Mostrar el gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)  # Asegúrate de tener un frame para el gráfico
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar los datos: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Interpolación y Regresión Lineal")

# Crear un frame para los inputs
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

# Etiqueta y campo de entrada para los días (X)
label_x = tk.Label(frame_input, text="Introduce los días (separados por coma):")
label_x.grid(row=0, column=0)
entry_x = tk.Entry(frame_input, width=40)
entry_x.grid(row=0, column=1)

# Etiqueta y campo de entrada para las alturas (Y)
label_y = tk.Label(frame_input, text="Introduce las alturas (separadas por coma, usa 'nan' para valores faltantes):")
label_y.grid(row=1, column=0)
entry_y = tk.Entry(frame_input, width=40)
entry_y.grid(row=1, column=1)

# Botón para procesar los datos
button_procesar = tk.Button(frame_input, text="Procesar Datos", command=procesar_datos)
button_procesar.grid(row=2, columnspan=2, pady=10)

# Crear un frame para los resultados
frame_resultados = tk.Frame(root)
frame_resultados.pack(pady=10)

# Etiqueta para mostrar los resultados
result_text = tk.StringVar()
label_resultados = tk.Label(frame_resultados, textvariable=result_text, justify=tk.LEFT)
label_resultados.pack()

# Crear un frame para el gráfico
frame_graph = tk.Frame(root)
frame_graph.pack(pady=10)

# Iniciar la interfaz
root.mainloop()
