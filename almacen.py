import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
import json
import os

# Ruta para los datos del almacén
DB_FOLDER = "DB"
ARTICLES_FILE = os.path.join(DB_FOLDER, "articles.json")

# Inicializar archivo de artículos
def initialize_articles_file():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)  # Crear carpeta si no existe
    if not os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, "w") as file:
            json.dump({}, file)  # Archivo vacío inicial

# Cargar nombres de artículos para los Combobox
def load_article_names():
    if not os.path.exists(ARTICLES_FILE):
        return []
    with open(ARTICLES_FILE, "r") as file:
        articles = json.load(file)
    return [article["name"] for code, article in articles.items() if "name" in article]

# Función para cargar artículos en la tabla
def load_articles_into_table(tree):
    if not os.path.exists(ARTICLES_FILE):
        return
    with open(ARTICLES_FILE, "r") as file:
        articles = json.load(file)
    # Limpiar la tabla antes de cargar datos
    for item in tree.get_children():
        tree.delete(item)
    # Insertar datos en la tabla
    for code, article in articles.items():
        tree.insert(
            "",
            "end",
            values=(
                code,
                article.get("name", ""),
                article.get("description", ""),
                article.get("category", ""),
                article.get("location", ""),
                article.get("quantity", 0),
            ),
        )

# Función para mostrar ventana de generar etiquetas
def generate_labels_window(article_name):
    def accept():
        messagebox.showinfo("Generar Etiquetas", f"Etiqueta generada para el artículo: {article_name}")
        label_window.destroy()

    def omit():
        messagebox.showinfo("Omitir", "Operación omitida.")
        label_window.destroy()

    label_window = tk.Toplevel()
    label_window.title("Generar Etiquetas")
    label_window.geometry("300x150")

    tk.Label(label_window, text="Generar etiquetas para artículos").pack(pady=10)
    tk.Label(label_window, text=f"Artículo: {article_name}").pack(pady=10)

    button_frame = tk.Frame(label_window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Aceptar", command=accept, width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Omitir", command=omit, width=10).pack(side="right", padx=5)

# Función para registrar nuevo artículo
def open_register_article_window(tree):
    def register_article():
        code = entry_code.get()
        name = entry_name.get()
        description = entry_description.get()
        category = entry_category.get()
        location = entry_location.get()

        if code and name and description and category and location:
            with open(ARTICLES_FILE, "r+") as file:
                articles = json.load(file)
                if code in articles:
                    messagebox.showerror("Error", "El código del artículo ya existe.")
                else:
                    articles[code] = {
                        "name": name,
                        "description": description,
                        "category": category,
                        "location": location,
                        "quantity": 0
                    }
                    file.seek(0)
                    json.dump(articles, file, indent=4)
                    messagebox.showinfo("Éxito", f"Artículo {name} registrado exitosamente.")
                    register_window.destroy()
                    load_articles_into_table(tree)  # Refrescar la tabla
                    generate_labels_window(name)  # Mostrar ventana de generar etiquetas
        else:
            messagebox.showerror("Error", "Por favor, llena todos los campos.")

    register_window = tk.Toplevel()
    register_window.title("Registrar Nuevo Artículo")
    register_window.geometry("400x350")

    tk.Label(register_window, text="Código del artículo:").pack(pady=5)
    entry_code = tk.Entry(register_window)
    entry_code.pack(pady=5)

    tk.Label(register_window, text="Nombre del artículo:").pack(pady=5)
    entry_name = tk.Entry(register_window)
    entry_name.pack(pady=5)

    tk.Label(register_window, text="Descripción:").pack(pady=5)
    entry_description = tk.Entry(register_window)
    entry_description.pack(pady=5)

    tk.Label(register_window, text="Categoría:").pack(pady=5)
    entry_category = tk.Entry(register_window)
    entry_category.pack(pady=5)

    tk.Label(register_window, text="Ubicación inicial:").pack(pady=5)
    entry_location = tk.Entry(register_window)
    entry_location.pack(pady=5)

    tk.Button(register_window, text="Registrar", command=register_article).pack(pady=10)

# Ventana principal del módulo de almacén
def open_almacen_window():
    initialize_articles_file()

    almacen_window = tk.Tk()
    almacen_window.title("Gestión de Almacén")
    almacen_window.geometry("800x500")

    main_frame = tk.Frame(almacen_window, padx=10, pady=10)
    main_frame.pack(fill="both", expand=True)

    # Tabla para mostrar artículos
    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(side="left", fill="both", expand=True)

    columns = ("Código", "Nombre", "Descripción", "Categoría", "Ubicación", "Cantidad")
    tree = Treeview(tree_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Cargar datos en la tabla al inicio
    load_articles_into_table(tree)

    # Botones a la derecha
    button_frame = tk.Frame(main_frame)
    button_frame.pack(side="right", fill="y", padx=10)

    tk.Button(
        button_frame, 
        text="Registrar Artículo", 
        command=lambda: open_register_article_window(tree), 
        width=20, 
        height=2
    ).pack(pady=5)

    tk.Button(
        button_frame, 
        text="Registrar Ingreso", 
        command=lambda: open_register_entry_window(tree), 
        width=20, 
        height=2
    ).pack(pady=5)

    tk.Button(
        button_frame, 
        text="Actualizar Existencias", 
        command=lambda: open_update_stock_window(tree), 
        width=20, 
        height=2
    ).pack(pady=5)

    almacen_window.mainloop()
