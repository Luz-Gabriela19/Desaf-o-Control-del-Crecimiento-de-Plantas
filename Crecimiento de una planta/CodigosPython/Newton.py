import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def diferencias_divididas(x, y):
    n = len(x)
    coeficientes = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        coeficientes[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            coeficientes[i][j] = (coeficientes[i+1][j-1] - coeficientes[i][j-1]) / (x[i+j] - x[i])
    
    return [coeficientes[0][i] for i in range(n)], coeficientes

def newton_interpolation(x_vals, y_vals, x_eval):
    detalles = ""
    coef, matriz = diferencias_divididas(x_vals, y_vals)
    n = len(coef)

    detalles += "=== DIFERENCIAS DIVIDIDAS ===\n"
    for i in range(n):
        for j in range(i+1):
            detalles += f"f[x{i}"
            for k in range(1, j+1):
                detalles += f",x{i+k}"
            detalles += f"] = {matriz[i][j]:.6f}\n"
    detalles += "\n"

    resultado = coef[0]
    term_string = f"{coef[0]:.6f}"
    detalles += f"P(x) = {coef[0]:.6f}"

    producto = 1
    for i in range(1, n):
        producto *= (x_eval - x_vals[i-1])
        term_val = coef[i] * producto
        resultado += term_val
        term_str = f"{coef[i]:.6f}"
        for j in range(i):
            term_str += f" * (x - {x_vals[j]})"
        detalles += f" + {coef[i]:.6f} * " + " * ".join([f"({x_eval} - {x_vals[j]})" for j in range(i)]) + f" = {term_val:.6f}\n"

    detalles += f"\n\nP({x_eval}) = {resultado:.6f}"
    return resultado, detalles

def calcular_newton():
    try:
        x_input = entry_x.get()
        y_input = entry_y.get()
        x_eval = float(entry_eval.get())

        x_vals = list(map(float, x_input.strip().split(',')))
        y_vals = list(map(float, y_input.strip().split(',')))

        if len(x_vals) != len(y_vals):
            messagebox.showerror("Error", "Las listas de X e Y deben tener la misma longitud.")
            return

        resultado, detalles = newton_interpolation(x_vals, y_vals, x_eval)
        label_resultado.config(text=f"P({x_eval}) = {resultado:.6f}")
        texto_detalle.delete('1.0', tk.END)
        texto_detalle.insert(tk.END, detalles)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------------- Interfaz Gráfica -----------------

root = tk.Tk()
root.title("Interpolación de Newton - Paso a Paso")
root.geometry("750x600")
root.configure(bg="#f0f0ff")

titulo = tk.Label(root, text="Interpolación por el Método de Newton", font=("Helvetica", 16, "bold"), bg="#f0f0ff", fg="#333")
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

ttk.Button(root, text="Calcular Interpolación", command=calcular_newton).pack(pady=10)

label_resultado = tk.Label(root, text="Resultado: ", font=("Helvetica", 14), bg="#f0f0ff")
label_resultado.pack()

texto_detalle = scrolledtext.ScrolledText(root, width=90, height=20, font=("Courier", 10))
texto_detalle.pack(padx=10, pady=10)

root.mainloop()
