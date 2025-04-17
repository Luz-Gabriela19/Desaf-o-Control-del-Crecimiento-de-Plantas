import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

def lagrange_interpolation_detallado(x_vals, y_vals, x_eval):
    n = len(x_vals)
    total = 0
    detalles = ""

    for i in range(n):
        xi, yi = x_vals[i], y_vals[i]
        detalles += f"\nL_{i}(x): "

        numerador = ""
        denominador = ""
        Li = 1

        for j in range(n):
            if j != i:
                numerador += f"(x - {x_vals[j]})"
                denominador += f"({xi} - {x_vals[j]})"
                Li *= (x_eval - x_vals[j]) / (xi - x_vals[j])

        producto = yi * Li
        total += producto

        detalles += f"{numerador} / {denominador}\n"
        detalles += f"L_{i}({x_eval}) = {Li:.6f}, y_{i} = {yi}, y_{i} * L_{i} = {producto:.6f}\n"

    detalles += f"\nP({x_eval}) = {total:.6f}"
    return total, detalles

def calcular_lagrange():
    try:
        x_input = entry_x.get()
        y_input = entry_y.get()
        x_eval = float(entry_eval.get())

        x_vals = list(map(float, x_input.strip().split(',')))
        y_vals = list(map(float, y_input.strip().split(',')))

        if len(x_vals) != len(y_vals):
            messagebox.showerror("Error", "Las listas de X e Y deben tener la misma longitud.")
            return

        resultado, detalles = lagrange_interpolation_detallado(x_vals, y_vals, x_eval)
        label_resultado.config(text=f"P({x_eval}) = {resultado:.6f}")
        texto_detalle.delete('1.0', tk.END)
        texto_detalle.insert(tk.END, detalles)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Interfaz Gráfica Mejorada ----------

root = tk.Tk()
root.title("Interpolación de Lagrange - Paso a Paso")
root.geometry("750x600")
root.configure(bg="#f0f0ff")

titulo = tk.Label(root, text="Interpolación por el Método de Lagrange", font=("Helvetica", 16, "bold"), bg="#f0f0ff", fg="#333")
titulo.pack(pady=10)

frame_inputs = ttk.Frame(root, padding="10")
frame_inputs.pack()

ttk.Label(frame_inputs, text="Valores de X (separados por coma):").grid(row=0, column=0, sticky="w")
entry_x = ttk.Entry(frame_inputs, width=60)
entry_x.grid(row=0, column=1, pady=5)

ttk.Label(frame_inputs, text="Valores de Y (separados por coma):").grid(row=1, column=0, sticky="w")
entry_y = ttk.Entry(frame_inputs, width=60)
entry_y.grid(row=1, column=1, pady=5)

ttk.Label(frame_inputs, text="Valor de X a evaluar:").grid(row=2, column=0, sticky="w")
entry_eval = ttk.Entry(frame_inputs, width=20)
entry_eval.grid(row=2, column=1, sticky="w", pady=5)

ttk.Button(root, text="Calcular Interpolación", command=calcular_lagrange).pack(pady=10)

label_resultado = tk.Label(root, text="Resultado: ", font=("Helvetica", 14), bg="#f0f0ff")
label_resultado.pack()

texto_detalle = scrolledtext.ScrolledText(root, width=90, height=20, font=("Courier", 10))
texto_detalle.pack(padx=10, pady=10)

root.mainloop()

