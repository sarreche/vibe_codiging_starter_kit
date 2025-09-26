import tkinter as tk
import random

# Lista de colores sugeridos (puedes agregar más en colors.txt)
colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6", "#E67E22", "#2ECC71"]

def change_color():
    # Elige un color al azar de la lista
    new_color = random.choice(colors)
    window.config(bg=new_color)
    label.config(text=f"Color: {new_color}", bg=new_color)

# Ventana principal
window = tk.Tk()
window.title("Color Mood Changer")
window.geometry("400x300")

# Etiqueta con mensaje inicial
label = tk.Label(window, text="Haz clic en el botón para cambiar de color!", font=("Arial", 14))
label.pack(pady=40)

# Botón
button = tk.Button(window, text="Click me!", font=("Arial", 12), command=change_color)
button.pack()

# Inicia la app
window.mainloop()
