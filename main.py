from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import sqlite3
import re

# ##############################################
# MODELO
# ##############################################

def conexion():
    con = sqlite3.connect("contactos.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS contactos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre varchar(20) NOT NULL,
             apellido real,
             correo real,
             numero real)
    """
    cursor.execute(sql)
    con.commit()

try:
    conexion()
    crear_tabla()
except:
    print("Hay un error")

def actualizar_treeview(mitreview):
    registro = mitreview.get_children()
    for contacto in registro:
        mitreview.delete(contacto)

    sql = "SELECT * FROM contactos ORDER BY id ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4]))

def alta(nombre, apellido, correo, numero, tree):
    cadena = nombre
    patron="^[A-Za-záéíóú]*$"
    if(re.match(patron, cadena)):
        print(nombre, apellido, correo, numero)
        con=conexion()
        cursor=con.cursor()
        data=(nombre, apellido, correo, numero)
        sql="INSERT INTO contactos(nombre, apellido, correo, numero) VALUES(?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print("Estoy en alta todo ok")
        actualizar_treeview(tree)
        mb.showinfo("Información", "Nuevo contacto agendado!")
    else:
        print("error en campo contacto")

def borrar(tree):
    valor = tree.selection()
    print(valor)
    item = tree.item(valor)
    print(item)
    print(item['text'])
    mi_id = item['text']

    con=conexion()
    cursor=con.cursor()
    #mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM contactos WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    respuesta=mb.askyesno("Cuidado", "¿Está seguro que quiere eliminat el contacto?")
    if respuesta==True:
        tree.delete(valor)
    

def consultar(con, mi_id, ):
    valor = tree.selection()
    item = tree.item(valor)
    #print(item['text'])
    mi_id = item['text']

    cursor = con.cursor()
    mi_id = int(mi_id)
    data = (mi_id,)
    sql = "SELECT * FROM contactos WHERE id =?;"
    cursor.execute(sql, data)

    items = cursor.fetchall()

    for item in items:
        print(item)
        mb.showinfo("Información de contacto", item)

def get_item_seleccionado():
    item_seleccionado = tree.selection()
    if item_seleccionado:
        item = tree.item(item_seleccionado)
        mi_id = item['text']
        return mi_id
    else:
        return None

def actualizar(con, mi_id, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_numero, tree):
    cursor = con.cursor()
    data = (nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_numero, mi_id)
    sql = "UPDATE contactos SET nombre=?, apellido=?, correo=?, numero=? WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()
    print("Contacto actualizado")
    actualizar_treeview(tree)


def actualizar_tree():
    mi_id = get_item_seleccionado()
    nuevo_nombre = nombre_val.get()
    nuevo_apellido = apellido_val.get()
    nuevo_correo = correo_val.get()
    nuevo_numero = numero_val.get()

    actualizar(conexion(), mi_id, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_numero, tree)
    mb.showinfo("Información", "El contacto ha sido actualizado!")

modo_claro = {
    'bg': 'white',
    'fg': 'black',
    'entry_bg': '#eee',
    'entry_fg': 'black',
    'btn_bg': '#ddd',
    'btn_fg': 'black'
}

modo_oscuro = {
    'bg': '#333',
    'fg': 'white',
    'entry_bg': '#555',
    'entry_fg': 'white',
    'btn_bg': '#444',
    'btn_fg': 'white'
}

modo_oscuro_activo = False

def cambiar_tema():
    global modo_oscuro_activo
    modo_oscuro_activo = not modo_oscuro_activo
    aplicar_cambiar_tema()

def aplicar_cambiar_tema():
    if modo_oscuro_activo:
        colores = modo_oscuro
    else:
        colores = modo_claro

    root.config(bg=colores['bg'])

    for widget in root.winfo_children():
        widget_type = widget.winfo_class()

        if widget_type == 'Label':
            widget.config(bg=colores['bg'], fg=colores['fg'])
        elif widget_type == 'Entry':
            widget.config(bg=colores['entry_bg'], fg=colores['entry_fg'], insertbackground=colores['fg'])
        elif widget_type == 'Button':
            widget.config(bg=colores['btn_bg'], fg=colores['btn_fg'])

# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("Agenda virtual")
        
titulo = Label(root, text="Bienvenido a tu agenda virtual!", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

nombre = Label(root, text="Nombre")
nombre.grid(row=1, column=0, sticky=W)
apellido=Label(root, text="Apellido")
apellido.grid(row=2, column=0, sticky=W)
correo=Label(root, text="Correo electrónico")
correo.grid(row=3, column=0, sticky=W)
numero=Label(root, text="Número de teléfono")
numero.grid(row=4, column=0, sticky=W)

nombre_val, apellido_val, correo_val, numero_val = StringVar(), StringVar(), StringVar(), IntVar(),
w_ancho = 20

entrada1 = Entry(root, textvariable = nombre_val, width = w_ancho) 
entrada1.grid(row = 1, column = 1)
entrada2 = Entry(root, textvariable = apellido_val, width = w_ancho) 
entrada2.grid(row = 2, column = 1)
entrada3 = Entry(root, textvariable = correo_val, width = w_ancho) 
entrada3.grid(row = 3, column = 1)
entrada4 = Entry(root, textvariable = numero_val, width = w_ancho) 
entrada4.grid(row = 4, column = 1)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)
tree["columns"]=("col1", "col2", "col3", "col4")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Nombre")
tree.heading("col2", text="Apellido")
tree.heading("col3", text="Correo electrónico")
tree.heading("col4", text="Numero de teléfono")
tree.grid(row=10, column=0, columnspan=4)

boton_alta = Button(root, text="Agendar Nuevo", command=lambda:alta(nombre_val.get(), apellido_val.get(), correo_val.get(), numero_val.get(), tree))
boton_alta.grid(row=6, column=0)

boton_borrar = Button(root, text="Borrar Contacto", command=lambda:borrar(tree))
boton_borrar.grid(row=7, column=0)

boton_consulta = Button(root, text="Consultar Contacto", command=lambda:consultar(conexion(), nombre_val.get()))
boton_consulta.grid(row=6, column=1)

boton_actualizar = Button(root, text="Actualizar Contacto", command=lambda:actualizar_tree())
boton_actualizar.grid(row=7, column=1)

boton_tema = Button(root, text="Cambiar Tema", command=lambda:cambiar_tema())
boton_tema.grid(row=3, column=3, columnspan=2)

aplicar_cambiar_tema()

root.mainloop()