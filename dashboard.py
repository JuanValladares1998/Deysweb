import tkinter as tk
import compras
import distribucion
from tkinter import messagebox


def open_dashboard(username):
    # Crear la ventana del dashboard
    dashboard = tk.Tk()
    dashboard.title("Dashboard Principal")
    dashboard.geometry("400x400")

    # Etiqueta de bienvenida
    label_welcome = tk.Label(dashboard, text=f"Bienvenido, {username}!", font=("Arial", 16))
    label_welcome.pack(pady=20)

    # Información del usuario
    label_info = tk.Label(dashboard, text=f"Usuario: {username}", font=("Arial", 12))
    label_info.pack(pady=10)

    # Funciones de los botones
    def open_almacen():
        import almacen  # Importar el módulo de almacén
        almacen.open_almacen_window()

    def open_compras():
        import compras  # Importar el módulo de compras
        compras.open_compras_window()

    def open_distribucion():
        distribucion.open_distribution_window()

    # Función para cerrar sesión
    def logout():
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?"):
            dashboard.destroy()  # Cierra la ventana del dashboard
            import main  # Regresa al login importando el archivo principal
            main.run_login()

    # Botones principales
    button_almacen = tk.Button(dashboard, text="Adquisición de Artículos", command=open_almacen, width=20, height=2)
    button_almacen.pack(pady=10)

    button_compras = tk.Button(dashboard, text="Recepción de Artículos", command=open_compras, width=20, height=2)
    button_compras.pack(pady=10)

    button_distribucion = tk.Button(dashboard, text="Gestión de Distribución", width=20, height=2, command=open_distribucion)
    button_distribucion.pack(pady=10)

    button_logout = tk.Button(dashboard, text="Cerrar Sesión", command=logout, width=20, height=2, bg="red", fg="white")
    button_logout.pack(pady=20)

    # Ejecutar la ventana
    dashboard.mainloop()
