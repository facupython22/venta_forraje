##########################################
# Programa de Gestion de Venta de Semillas
##########################################

######################### Modulos a utilizar #########################################
######################################################################################
import tkinter as tk                # ---> Para la GUI (Interfaz Grafica de Usuario).
from tkinter import ttk,messagebox  # ---> Para la notificacion de eventos realizados.
import sqlite3                      # ---> Para Generar la Base de Datos.
import re                           # ---> Para Validar campos (Telefono Cliente).
######################################################################################

########################## Funciones para el CRUD ####################################
######################################################################################
def conectar_bd():
    return sqlite3.connect("venta_semillas.db")


def crear_tabla():
    conex = conectar_bd()
    cursor = conex.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS ventas 
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cultivar TEXT,
        cantidad INTEGER,
        cliente TEXT,
        telefono TEXT,
        vendedor TEXT,
        fecha TEXT
        )
        """)
    conex.commit()
    conex.close()
crear_tabla()

def mostrar_ventas():
    for item in ventas_treeview.get_children():
        ventas_treeview.delete(item)
    conex = conectar_bd()
    cursor = conex.cursor()
    cursor.execute('SELECT * FROM ventas')
    ventas = cursor.fetchall()
    conex.close()

    for venta in ventas:
        ventas_treeview.insert("", tk.END, values=venta)

def limpiar_campos():
    cultivar_combobox.set('')
    cantidad_entry.delete(0, tk.END)
    cliente_entry.delete(0, tk.END)
    telefono_entry.delete(0, tk.END)
    vendedor_combobox.set('')
    fecha_entry.delete(0, tk.END)

def eliminar_venta():
    seleccionar_item = ventas_treeview.selection()
    if seleccionar_item:
        venta_id = ventas_treeview.item(seleccionar_item, 'values')[0]
        conex= conectar_bd()
        cursor = conex.cursor()
        cursor.execute('DELETE FROM ventas WHERE id = ?', (venta_id,))
        conex.commit()
        conex.close()
        mostrar_ventas()
        messagebox.showinfo("EXITO", "Venta eliminada.")
    else:
        messagebox.showwarning("¡ERROR!", "Seleccione una venta para eliminar.")

def agregar_venta():
    cultivar=cultivar_combobox.get()
    cantidad=cantidad_entry.get()
    cliente=cliente_entry.get()
    telefono=telefono_entry.get()
    vendedor=vendedor_combobox.get()
    fecha=fecha_entry.get()

    if not re.fullmatch(r'\d{10}', telefono):
        messagebox.showwarning("¡ERROR!", "Número de teléfono inválido. El número debe contener 10 dígitos.")
        return

    if cultivar and cantidad and cliente and vendedor and fecha:
        conex = conectar_bd()
        cursor = conex.cursor()
        cursor.execute(""" INSERT INTO ventas (cultivar,cantidad,cliente,telefono,vendedor,fecha)
        VALUES (?,?,?,?,?,?)
        """, (cultivar,cantidad,cliente,telefono,vendedor,fecha))
        conex.commit()
        conex.close()

        mostrar_ventas()
        limpiar_campos()

        messagebox.showinfo("¡Felicidades!","Nueva venta registrada!")
    else:
        messagebox.showinfo("¡Ops!","Algo salió mal. Revisa que todos los campos estén completos.")

def modificar_venta():
    seleccionar_item = ventas_treeview.selection()
    if seleccionar_item:
        venta_id = ventas_treeview.item(seleccionar_item, 'values')[0]
        cultivo_actual = cultivar_combobox.get()
        cantidad_actual = cantidad_entry.get()
        cliente_actual = cliente_entry.get()
        telefono_actual = telefono_entry.get()
        vendedor_actual = vendedor_combobox.get()
        fecha_actual = fecha_entry.get()

        conex = conectar_bd()
        cursor = conex.cursor()
        cursor.execute('SELECT * FROM ventas WHERE id = ?', (venta_id,))
        venta = cursor.fetchone()
        conex.close()

        cultivo = cultivo_actual if cultivo_actual else venta[1]
        cantidad = cantidad_actual if cantidad_actual else venta[2]
        cliente = cliente_actual if cliente_actual else venta[3]
        telefono = telefono_actual if telefono_actual else venta[4]
        vendedor = vendedor_actual if vendedor_actual else venta[5]
        fecha = fecha_actual if fecha_actual else venta[6]

        conex = conectar_bd()
        cursor = conex.cursor()
        cursor.execute('''
        UPDATE ventas
        SET cultivar = ?, cantidad = ?, cliente = ?, telefono = ?, vendedor = ?, fecha = ?
        WHERE id = ?
        ''', (cultivo, cantidad, cliente, telefono, vendedor, fecha, venta_id))
        conex.commit()
        conex.close()
        mostrar_ventas()
        limpiar_campos()
        messagebox.showinfo("¡Felicidades!", "Venta modificada exitosamente.")
    else:
        messagebox.showwarning("¡ERROR!", "Seleccione una venta para modificar.")

#################### Desarrollo de la GUI (Interfaz Gráfica de Usuario #########################
################################################################################################

color_fondo = "#B1DB9E"
color_texto = "#333333"

root = tk.Tk()
root.title("Catedra Forrajicultura - UNNE")
root.configure(bg=color_fondo)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

# titulo
titulo_label = tk.Label(root, text="Facultad de Ciencias Agrarias - UNNE", font=("Arial", 16), bg=color_fondo, fg=color_texto)
titulo_label.grid(row=0, column=0, columnspan=4, pady=10)

# cultivar (combobox)
tk.Label(root, text="Cultivar:", bg=color_fondo, fg=color_texto).grid(row=1, column=0, sticky="e")
cultivar_combobox = ttk.Combobox(root, values=["Boyero FCA", "Chané FCA", "Cambá FCA"], width=15)
cultivar_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Agregar Venta", command=agregar_venta).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# cantidad

tk.Label(root, text="Cantidad (KG):", bg=color_fondo, fg=color_texto).grid(row=2, column=0, sticky="e")
cantidad_entry = tk.Entry(root, width=15)
cantidad_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

def validar_num(a):
    if a.isdigit() or a =="":
        return True
    else:
        return False

cantidad_valid = root.register(validar_num)
cantidad_entry.config(validate="key", validatecommand=(cantidad_valid, '%P'))

# ventas
tk.Button(root, text="Ver Ventas", command=mostrar_ventas).grid(row=2, column=2, padx=5, pady=5, sticky="ew")

# cliente
tk.Label(root, text="Nombre del Cliente:", bg=color_fondo, fg=color_texto).grid(row=3, column=0, sticky="e")
cliente_entry = tk.Entry(root, width=15)
cliente_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# eliminar
tk.Button(root, text="Eliminar Venta", command=eliminar_venta).grid(row=3, column=2, padx=5, pady=5, sticky="ew")

# telefono
tk.Label(root, text="Teléfono del Cliente:", bg=color_fondo, fg=color_texto).grid(row=4, column=0, sticky="e")
telefono_entry = tk.Entry(root, width=15)
telefono_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

def validar_telef(b):
    if b.isdigit() or b =="":
        return True
    else:
        return False

telefono_valid = root.register(validar_telef)
telefono_entry.config(validate="key", validatecommand=(cantidad_valid, '%P'))

#modificar
tk.Button(root, text="Modificar Venta", command=modificar_venta).grid(row=4, column=2, padx=5, pady=5, sticky="ew")

# vendedor (combobox)
tk.Label(root, text="Nombre del Vendedor:", bg=color_fondo, fg=color_texto).grid(row=5, column=0, sticky="e")
vendedor_combobox = ttk.Combobox(root, values=["Alex", "Florencia", "Andrea", "Carlos"], width=15)
vendedor_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

# fecha
"""
Tuve inconvenientes con esta parte tanto con el 
datepicker como con el datetime preferí hacerlo de esta 
forma por falta de tiempo para ver los errores. 
"""
tk.Label(root, text="Fecha de Venta (día/mes/año):", bg=color_fondo, fg=color_texto).grid(row=6, column=0, sticky="e")
fecha_entry = tk.Entry(root, width=15)
fecha_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

#############################################################
########### Treeview para los datos ###################
#############################################################

ventas_treeview = ttk.Treeview(root, columns=("ID", "Cultivar", "Cantidad", "Cliente", "Telefono", "Vendedor", "Fecha"), show="headings")
ventas_treeview.heading("ID", text="ID")
ventas_treeview.heading("Cultivar", text="Cultivar")
ventas_treeview.heading("Cantidad", text="Cantidad (KG)")
ventas_treeview.heading("Cliente", text="Cliente")
ventas_treeview.heading("Telefono", text="Telefono")
ventas_treeview.heading("Vendedor", text="Vendedor")
ventas_treeview.heading("Fecha", text="Fecha")

ventas_treeview.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

root.mainloop()

"""
El programa lo hice pensando en la catedra de la facultad donde trabajo,
en la misma contamos con 3 cultivares inscriptos en el INASE para la 
venta a productores. 
Los vendedores son los integrantes de la catedra, mis jefes.
Los registros de venta se manejaban con una tabla en excel.

PD: Estuve rindiendo mis ultimas materias y recien la semana antes de navidad me puse a tiro 
con esto. Hay cosas que me hubiese gustado implementar, pero bueno esto es todo lo que pude.

Que tengas un buen comienzo de año Juan, Saludos!

"""
