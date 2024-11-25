import tkinter as tk
from tkinter import messagebox
import json
import os
import dashboard  # Importar el archivo del dashboard

# Ruta para la carpeta DB y el archivo JSON
DB_FOLDER = "DB"
USER_FILE = os.path.join(DB_FOLDER, "users.json")

# Crear la carpeta DB y archivo JSON con el usuario inicial
def initialize_user_file():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)  # Crear carpeta DB si no existe
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as file:
            # Usuario inicial: usuario1, password: 123456
            json.dump({"usuario1": "123456"}, file)

# Función para validar el login
def validate_login(username, password):
    with open(USER_FILE, "r") as file:
        users = json.load(file)
    if username in users and users[username] == password:
        return True
    return False

# Función para manejar el botón de login
def login():
    username = entry_username.get()
    password = entry_password.get()
    if validate_login(username, password):
        root.destroy()  # Cierra la ventana de login
        dashboard.open_dashboard(username)  # Abrir el dashboard
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Inicializar el archivo de usuarios
initialize_user_file()

# Función principal para ejecutar el login
def run_login():
    global root, entry_username, entry_password

    # Crear la ventana principal de tkinter
    root = tk.Tk()
    root.title("Sistema de Login")
    root.geometry("300x200")

    # Etiqueta y entrada para el nombre de usuario
    label_username = tk.Label(root, text="Usuario:")
    label_username.pack(pady=5)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)

    # Etiqueta y entrada para la contraseña
    label_password = tk.Label(root, text="Contraseña:")
    label_password.pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    # Botón de login
    button_login = tk.Button(root, text="Iniciar Sesión", command=login)
    button_login.pack(pady=10)

    # Ejecutar la ventana principal
    root.mainloop()

# Ejecutar la función principal al iniciar el archivo
if __name__ == "__main__":
    run_login()
