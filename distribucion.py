import tkinter as tk
from tkinter import messagebox, ttk
import random
import os
import json

# Archivo de datos para las entregas
DB_FOLDER = "DB"
DELIVERIES_FILE = os.path.join(DB_FOLDER, "deliveries.json")

# Inicializar archivo de entregas
def initialize_deliveries_file():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    if not os.path.exists(DELIVERIES_FILE):
        with open(DELIVERIES_FILE, "w") as file:
            json.dump([], file)  # Lista vacía inicial

# Cargar entregas en la tabla
def load_deliveries_into_table(tree):
    if not os.path.exists(DELIVERIES_FILE):
        return
    with open(DELIVERIES_FILE, "r") as file:
        deliveries = json.load(file)
    # Limpiar la tabla antes de cargar datos
    for item in tree.get_children():
        tree.delete(item)
    # Insertar datos en la tabla
    for i, delivery in enumerate(deliveries, start=1):
        tree.insert(
            "",
            "end",
            values=(
                i,
                delivery.get("destination", ""),
                delivery.get("priority", ""),
                delivery.get("vehicle", ""),
                delivery.get("status", ""),
                delivery.get("incident", ""),
                delivery.get("observations", ""),
            ),
        )

# Función para planificar rutas de entrega
def open_plan_routes_window(tree):
    def plan_route():
        destination = entry_destination.get()
        priority = combobox_priority.get()
        if destination and priority:
            new_delivery = {
                "destination": destination,
                "priority": priority,
                "vehicle": "No asignado",
                "status": "Preparando paquete",
                "incident": "Ninguna",
                "observations": "",
            }
            with open(DELIVERIES_FILE, "r+") as file:
                deliveries = json.load(file)
                deliveries.append(new_delivery)
                file.seek(0)
                json.dump(deliveries, file, indent=4)
            messagebox.showinfo("Éxito", f"Ruta planificada hacia {destination} con prioridad {priority}.")
            plan_window.destroy()
            load_deliveries_into_table(tree)
        else:
            messagebox.showerror("Error", "Completa todos los campos.")

    plan_window = tk.Toplevel()
    plan_window.title("Planificar Rutas de Entrega")
    plan_window.geometry("400x300")

    tk.Label(plan_window, text="Destino:").pack(pady=10)
    entry_destination = tk.Entry(plan_window, width=40)
    entry_destination.pack(pady=10)

    tk.Label(plan_window, text="Prioridad:").pack(pady=10)
    combobox_priority = ttk.Combobox(plan_window, values=["Alta", "Media", "Baja"], state="readonly")
    combobox_priority.pack(pady=10)

    tk.Button(plan_window, text="Planificar", command=plan_route, width=15).pack(pady=20)

# Función para asignar entrega a vehículo
def open_assign_delivery_window(tree):
    def assign_delivery():
        vehicle = combobox_vehicle.get()
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una entrega para asignar.")
            return
        if vehicle:
            with open(DELIVERIES_FILE, "r+") as file:
                deliveries = json.load(file)
                delivery_index = int(tree.item(selected_item, "values")[0]) - 1
                deliveries[delivery_index]["vehicle"] = vehicle
                file.seek(0)
                json.dump(deliveries, file, indent=4)
            messagebox.showinfo("Éxito", f"Entrega asignada al vehículo {vehicle}.")
            assign_window.destroy()
            load_deliveries_into_table(tree)
        else:
            messagebox.showerror("Error", "Selecciona un vehículo.")

    assign_window = tk.Toplevel()
    assign_window.title("Asignar Entrega a Vehículo")
    assign_window.geometry("400x200")

    tk.Label(assign_window, text="Vehículo:").pack(pady=10)
    combobox_vehicle = ttk.Combobox(assign_window, values=["Camión 1", "Camión 2", "Camión 3"], state="readonly")
    combobox_vehicle.pack(pady=10)

    tk.Button(assign_window, text="Asignar", command=assign_delivery, width=15).pack(pady=20)

# Función para generar documentos de transporte
def open_generate_documents_window(tree):
    def generate_documents():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una entrega para generar documentos.")
            return
        delivery_index = int(tree.item(selected_item, "values")[0]) - 1
        with open(DELIVERIES_FILE, "r") as file:
            deliveries = json.load(file)
            delivery = deliveries[delivery_index]
        messagebox.showinfo(
            "Documentos Generados",
            f"Documentos generados para la entrega:\nDestino: {delivery['destination']}\nVehículo: {delivery['vehicle']}"
        )
        documents_window.destroy()

    documents_window = tk.Toplevel()
    documents_window.title("Generar Documentos de Transporte")
    documents_window.geometry("400x150")

    tk.Label(documents_window, text="Generar documentos para la entrega seleccionada").pack(pady=20)
    tk.Button(documents_window, text="Generar", command=generate_documents, width=15).pack(pady=20)

# Función para monitorear entregas
def open_monitor_deliveries_window():
    def show_random_status():
        statuses = [
            "Preparando paquete",
            "Entregado al courier",
            "En camino",
            "Retraso en la entrega",
            "Entregado",
        ]
        random_status = random.choice(statuses)
        messagebox.showinfo("Estado de Entrega", f"Estado actual: {random_status}")

    monitor_window = tk.Toplevel()
    monitor_window.title("Monitorear Entregas en Tiempo Real")
    monitor_window.geometry("400x150")

    tk.Label(monitor_window, text="Monitoreo en tiempo real de entregas").pack(pady=20)
    tk.Button(monitor_window, text="Ver Estado", command=show_random_status, width=20).pack(pady=20)

# Función para registrar incidencias
def open_register_incidents_window(tree):
    def register_incident():
        incident = combobox_incident.get()
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una entrega para registrar la incidencia.")
            return
        if incident:
            delivery_index = int(tree.item(selected_item, "values")[0]) - 1
            with open(DELIVERIES_FILE, "r+") as file:
                deliveries = json.load(file)
                deliveries[delivery_index]["incident"] = incident
                file.seek(0)
                json.dump(deliveries, file, indent=4)
            messagebox.showinfo("Éxito", f"Incidencia registrada: {incident}")
            incidents_window.destroy()
            load_deliveries_into_table(tree)
        else:
            messagebox.showerror("Error", "Selecciona una incidencia.")

    incidents_window = tk.Toplevel()
    incidents_window.title("Registrar Incidencias")
    incidents_window.geometry("400x200")

    tk.Label(incidents_window, text="Tipo de Incidencia:").pack(pady=10)
    combobox_incident = ttk.Combobox(incidents_window, values=["Retraso", "Devolución", "Daño"], state="readonly")
    combobox_incident.pack(pady=10)

    tk.Button(incidents_window, text="Registrar", command=register_incident, width=15).pack(pady=20)

# Función para generar reportes de eficiencia
def open_generate_efficiency_report_window(tree):
    messagebox.showinfo("Reporte", "Reporte de eficiencia generado (simulación).")

# Ventana principal del módulo de distribución
def open_distribution_window():
    initialize_deliveries_file()

    distribution_window = tk.Tk()
    distribution_window.title("Gestión de Distribución")
    distribution_window.geometry("900x600")

    tk.Label(distribution_window, text="Gestión de Distribución", font=("Arial", 16)).pack(pady=10)

    table_frame = tk.Frame(distribution_window)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("#", "Destino", "Prioridad", "Vehículo", "Estado", "Incidencia", "Observaciones")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.pack(fill="both", expand=True)
    load_deliveries_into_table(tree)

    button_frame = tk.Frame(distribution_window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Planificar Rutas de Entrega", width=25, height=2,
              command=lambda: open_plan_routes_window(tree)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Asignar Entrega a Vehículo", width=25, height=2,
              command=lambda: open_assign_delivery_window(tree)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Generar Documentos de Transporte", width=25, height=2,
              command=lambda: open_generate_documents_window(tree)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Monitorear Entregas en Tiempo Real", width=25, height=2,
              command=open_monitor_deliveries_window).pack(side="left", padx=5)
    tk.Button(button_frame, text="Registrar Incidencias en la Distribución", width=25, height=2,
              command=lambda: open_register_incidents_window(tree)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Generar Reportes de Eficiencia", width=25, height=2,
              command=lambda: open_generate_efficiency_report_window(tree)).pack(side="left", padx=5)

    distribution_window.mainloop()
