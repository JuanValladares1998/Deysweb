import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Ruta para almacenar las órdenes de compra
DB_FOLDER = "DB"
ORDERS_FILE = os.path.join(DB_FOLDER, "orders.json")

# Inicializar archivos necesarios
def initialize_orders_file():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)  # Crear carpeta si no existe
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w") as file:
            json.dump([], file)  # Lista vacía inicial para órdenes

# Cargar órdenes de compra en la tabla
def load_orders_into_table(tree):
    if not os.path.exists(ORDERS_FILE):
        return
    with open(ORDERS_FILE, "r") as file:
        orders = json.load(file)
    # Limpiar la tabla antes de cargar datos
    for item in tree.get_children():
        tree.delete(item)
    # Insertar datos en la tabla
    for i, order in enumerate(orders, start=1):
        tree.insert(
            "",
            "end",
            values=(
                i,
                order["provider"],
                order["article"],
                order["quantity"],
                order["unit_price"],
                order["total_price"],
                order["observations"],
            ),
        )

# Ventana de formulario para registrar orden de compra
def open_register_order_window(tree):
    def save_order():
        provider = entry_provider.get()
        article = entry_article.get()
        quantity = entry_quantity.get()
        unit_price = entry_unit_price.get()
        observations = entry_observations.get("1.0", "end-1c").strip()

        if provider and article and quantity.isdigit() and unit_price.replace('.', '', 1).isdigit():
            order_data = {
                "provider": provider,
                "article": article,
                "quantity": int(quantity),
                "unit_price": float(unit_price),
                "total_price": int(quantity) * float(unit_price),
                "observations": observations,
            }
            with open(ORDERS_FILE, "r+") as file:
                orders = json.load(file)
                orders.append(order_data)
                file.seek(0)
                json.dump(orders, file, indent=4)
            messagebox.showinfo("Éxito", f"Orden registrada para el proveedor: {provider}")
            register_window.destroy()
            load_orders_into_table(tree)  # Actualizar la tabla
        else:
            messagebox.showerror("Error", "Completa todos los campos correctamente.")

    register_window = tk.Toplevel()
    register_window.title("Registrar Orden de Compra")
    register_window.geometry("500x450")

    tk.Label(register_window, text="Proveedor:").pack(pady=5)
    entry_provider = tk.Entry(register_window, width=40)
    entry_provider.pack(pady=5)

    tk.Label(register_window, text="Artículo:").pack(pady=5)
    entry_article = tk.Entry(register_window, width=40)
    entry_article.pack(pady=5)

    tk.Label(register_window, text="Cantidad:").pack(pady=5)
    entry_quantity = tk.Entry(register_window, width=40)
    entry_quantity.pack(pady=5)

    tk.Label(register_window, text="Precio Unitario:").pack(pady=5)
    entry_unit_price = tk.Entry(register_window, width=40)
    entry_unit_price.pack(pady=5)

    tk.Label(register_window, text="Observaciones:").pack(pady=5)
    entry_observations = tk.Text(register_window, width=40, height=5)
    entry_observations.pack(pady=5)

    tk.Button(register_window, text="Registrar", command=save_order, width=15, height=2).pack(pady=20)

# Ventana de formulario para confirmar recepción de artículos
def open_confirm_reception_window():
    def confirm_reception():
        order_id = entry_order_id.get()
        if order_id:
            messagebox.showinfo("Confirmación", f"Recepción confirmada para la orden: {order_id}.")
            confirm_window.destroy()
        else:
            messagebox.showerror("Error", "Por favor, ingresa el ID de la orden.")

    confirm_window = tk.Toplevel()
    confirm_window.title("Confirmar Recepción de Artículos")
    confirm_window.geometry("400x200")

    tk.Label(confirm_window, text="ID de la Orden:").pack(pady=10)
    entry_order_id = tk.Entry(confirm_window, width=30)
    entry_order_id.pack(pady=10)

    tk.Button(confirm_window, text="Confirmar", command=confirm_reception, width=15).pack(pady=20)

# Ventana de formulario para inspeccionar calidad de los artículos
def open_inspect_quality_window():
    def inspect_quality():
        article_name = entry_article_name.get()
        result = combobox_result.get()
        if article_name and result:
            messagebox.showinfo("Inspección", f"Calidad de {article_name} registrada como: {result}.")
            inspect_window.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    inspect_window = tk.Toplevel()
    inspect_window.title("Inspeccionar Calidad de los Artículos")
    inspect_window.geometry("400x250")

    tk.Label(inspect_window, text="Nombre del Artículo:").pack(pady=10)
    entry_article_name = tk.Entry(inspect_window, width=30)
    entry_article_name.pack(pady=10)

    tk.Label(inspect_window, text="Resultado de la Inspección:").pack(pady=10)
    combobox_result = ttk.Combobox(inspect_window, values=["Aprobado", "Rechazado"], state="readonly")
    combobox_result.pack(pady=10)

    tk.Button(inspect_window, text="Registrar", command=inspect_quality, width=15).pack(pady=20)

# Ventana de formulario para actualizar estado de orden de compra
def open_update_order_status_window():
    def update_status():
        order_id = entry_order_id.get()
        new_status = combobox_status.get()
        if order_id and new_status:
            messagebox.showinfo("Actualización", f"Estado de la orden {order_id} actualizado a: {new_status}.")
            update_window.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    update_window = tk.Toplevel()
    update_window.title("Actualizar Estado de Orden de Compra")
    update_window.geometry("400x250")

    tk.Label(update_window, text="ID de la Orden:").pack(pady=10)
    entry_order_id = tk.Entry(update_window, width=30)
    entry_order_id.pack(pady=10)

    tk.Label(update_window, text="Nuevo Estado:").pack(pady=10)
    combobox_status = ttk.Combobox(update_window, values=["En proceso", "Completada", "Pendiente"], state="readonly")
    combobox_status.pack(pady=10)

    tk.Button(update_window, text="Actualizar", command=update_status, width=15).pack(pady=20)

# Ventana de formulario para gestionar devoluciones
def open_manage_returns_window():
    def manage_return():
        article_name = entry_article_name.get()
        reason = entry_reason.get("1.0", "end-1c").strip()
        if article_name and reason:
            messagebox.showinfo("Devolución", f"Devolución registrada para {article_name}.\nRazón: {reason}.")
            returns_window.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    returns_window = tk.Toplevel()
    returns_window.title("Gestionar Devoluciones")
    returns_window.geometry("400x300")

    tk.Label(returns_window, text="Nombre del Artículo:").pack(pady=10)
    entry_article_name = tk.Entry(returns_window, width=30)
    entry_article_name.pack(pady=10)

    tk.Label(returns_window, text="Razón de la Devolución:").pack(pady=10)
    entry_reason = tk.Text(returns_window, width=40, height=5)
    entry_reason.pack(pady=10)

    tk.Button(returns_window, text="Registrar", command=manage_return, width=15).pack(pady=20)

# Ventana de formulario para generar informe de proveedores
def open_generate_supplier_report_window():
    def generate_report():
        messagebox.showinfo("Informe", "Informe de proveedores generado exitosamente (simulación).")
        report_window.destroy()

    report_window = tk.Toplevel()
    report_window.title("Generar Informe de Proveedores")
    report_window.geometry("400x150")

    tk.Label(report_window, text="Generar informe de proveedores").pack(pady=20)
    tk.Button(report_window, text="Generar", command=generate_report, width=15).pack(pady=20)

# Ventana principal del módulo de Compras
def open_compras_window():
    initialize_orders_file()

    compras_window = tk.Tk()
    compras_window.title("Gestión de Compras")
    compras_window.geometry("900x600")

    # Título
    tk.Label(compras_window, text="Gestión de Compras", font=("Arial", 16)).pack(pady=10)

    # Frame para la tabla
    table_frame = tk.Frame(compras_window)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Tabla para mostrar órdenes de compra
    columns = ("#", "Proveedor", "Artículo", "Cantidad", "Precio Unitario", "Precio Total", "Observaciones")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Configurar encabezados de la tabla
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.pack(fill="both", expand=True)

    # Cargar datos iniciales en la tabla
    load_orders_into_table(tree)

    # Frame para los botones
    button_frame = tk.Frame(compras_window)
    button_frame.pack(pady=10)

    # Botones para funcionalidades
    tk.Button(button_frame, text="Registrar Orden de Compra", width=25, height=2,
              command=lambda: open_register_order_window(tree)).pack(side="left", padx=10)
    tk.Button(button_frame, text="Confirmar Recepción de Artículos", width=25, height=2,
              command=open_confirm_reception_window).pack(side="left", padx=10)
    tk.Button(button_frame, text="Inspeccionar Calidad de los Artículos", width=25, height=2,
              command=open_inspect_quality_window).pack(side="left", padx=10)
    tk.Button(button_frame, text="Actualizar Estado de Orden de Compra", width=25, height=2,
              command=open_update_order_status_window).pack(side="left", padx=10)
    tk.Button(button_frame, text="Gestionar Devoluciones", width=25, height=2,
              command=open_manage_returns_window).pack(side="left", padx=10)
    tk.Button(button_frame, text="Generar Informe de Proveedores", width=25, height=2,
              command=open_generate_supplier_report_window).pack(side="left", padx=10)

    compras_window.mainloop()
