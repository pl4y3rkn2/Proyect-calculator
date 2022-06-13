from email import message
from pickle import READONLY_BUFFER
from sqlite3 import Cursor, connect
import tkinter as tk
from tkinter import LEFT, Label, Tk, ttk
import tkinter
from tkinter import messagebox
import mysql.connector
from datetime import datetime


#Opciones de la ventana
ventana = tk.Tk() #Ventana como objeto variable
ventana.title("Calculadora de 3 cuentas") #Cambiar el nombre de la ventana
ventana.config(width=300, height=250, bg="grey") #tamaño y configuracion de la ventana

#Cajas de texto y label
label1 = Label(ventana, text="Nivek2")
label1.pack(side=LEFT)
label1.place(x=20, y=20)
label1.config(bg="grey")
entry1 = ttk.Entry(justify=tk.LEFT, width=10) #caja de texto
entry1.place(x=65, y=20)
label2 = Label(ventana, text="Dosnet2")
label2.pack(side=LEFT)
label2.place(x=20, y=40)
label2.config(bg="grey")
entry2 = ttk.Entry(justify=tk.LEFT, width=10) #caja de texto
entry2.place(x=65, y=40)
label3 = Label(ventana, text="Meca")
label3.pack(side=LEFT)
label3.place(x=20, y=60)
label3.config(bg="grey")
entry3 = ttk.Entry(justify=tk.LEFT, width=10) #caja de texto
entry3.place(x=65, y=60)
label4 = Label(ventana, text="Valor oro/$")
label4.pack(side=LEFT)
label4.place(x=150, y=20)
label4.config(bg="grey")
entry4 = ttk.Entry(justify=tk.LEFT, width=10) #caja de texto
entry4.place(x=200, y=20)
totalsinporcentaje = ttk.Entry(justify=tk.LEFT, width=12, takefocus=False, state="normal") #caja de texto
totalsinporcentaje.place(x=20, y=100)
labeltotalsin = Label(ventana, text="Total de oro acumulado")
labeltotalsin.pack(side=LEFT)
labeltotalsin.place(x=100, y=100)
labeltotalsin.config(bg="grey")
totalconporcentaje = ttk.Entry(justify=tk.LEFT, width=12, takefocus=False, state="normal") #caja de texto
totalconporcentaje.place(x=20, y=120)
labeltotalcon = Label(ventana, text="Total de oro menos 5%")
labeltotalcon.pack(side=LEFT)
labeltotalcon.place(x=100, y=120)
labeltotalcon.config(bg="grey")
dolarpororo = ttk.Entry(justify=tk.LEFT, width=12, takefocus=False, state="normal") #caja de texto
dolarpororo.place(x=20, y=140)
labeldolarpororo = Label(ventana, text="$/oro")#label
labeldolarpororo.pack(side=LEFT)
labeldolarpororo.place(x=100, y=140)
labeldolarpororo.config(bg="grey")

# Funcion de Guardado
try:
    f = open("oro.txt")
    entry1.insert(0, int(f.readline()))
    entry2.insert(0, int(f.readline()))
    entry3.insert(0, int(f.readline()))
    entry4.insert(0, float(f.readline()))
    totalsinporcentaje.insert(0, int(f.readline()))
    totalconporcentaje.insert(0, float(f.readline()))
    dolarpororo.insert(0, float(f.readline()))    
    f.close()
except ValueError:
    entry1.insert(0, int(0))
    entry2.insert(0, int(0))
    entry3.insert(0, int(0))
    entry4.insert(0, float(0))
    totalsinporcentaje.insert(0, int(0))
    totalconporcentaje.insert(0, float(0))
    dolarpororo.insert(0, float(0))
# Funcion de botones

def suma():
    try:
        suma1 = int(entry1.get())
        suma2 = int(entry2.get())
        suma3 = int(entry3.get())
        precio = float(entry4.get())
        totalsuma = suma1+suma2+suma3
        totalsinporcentaje.delete(0,tk.END)
        totalconporcentaje.delete(0,tk.END)
        dolarpororo.delete(0,tk.END)
        totalsinporcentaje.insert(0, totalsuma)
        totalconporcentaje.insert(0, round(totalsuma*0.95,2))
        totalsuma *= 0.95
        dolarpororo.insert(0, round(totalsuma/1000*precio,2))
    except ValueError:
        messagebox.showinfo("Error de Calculo", "solo pueden calcular numero enteros")
        

def limpiar ():
    pregunta=messagebox.askquestion("Limpiar","¿Deseas Borrar todos los datos?")
    if pregunta=="yes":
        entry1.delete(0,tk.END)
        entry2.delete(0,tk.END)
        entry3.delete(0,tk.END)
        entry4.delete(0,tk.END)
        totalsinporcentaje.delete(0,tk.END)
        totalconporcentaje.delete(0,tk.END)
        dolarpororo.delete(0,tk.END)
        entry1.insert(0, int(0))
        entry2.insert(0, int(0))
        entry3.insert(0, int(0))
        entry4.insert(0, int(0))
        totalsinporcentaje.insert(0, int(0))
        totalconporcentaje.insert(0, int(0))
        dolarpororo.insert(0, float(0))

def salir ():
    pregunta=messagebox.askquestion("Salir","¿Deseas cerrar la aplicación?")
    if pregunta=="yes":
        ventana.destroy()
    
def guardar():
    if totalsinporcentaje.get()!="0":

        #Guardado de datos local de la aplicacion
        f=open("oro.txt", "w")
        f.write(entry1.get()+"\n")
        f.write(entry2.get()+"\n")
        f.write(entry3.get()+"\n")
        f.write(entry4.get()+"\n")
        f.write(totalsinporcentaje.get()+"\n")
        f.write(totalconporcentaje.get()+"\n")
        f.write(dolarpororo.get()+"\n")
        f.close()

        #connecion a la base de datos, guardados de datos y otros
        conexion = mysql.connector.connect(user="root", password="", host="localhost", database="db", port="3306")
        cursor = conexion.cursor()
        if conexion != "":
            sqlsave = "INSERT INTO `datos` (`cuenta1`, `cuenta2`, `cuenta3`, `DG`, `total`, `fecha`) VALUES ('"+entry1.get()+"', '"+entry2.get()+"', '"+entry3.get()+"', '"+entry4.get()+"', '"+totalsinporcentaje.get()+"', '"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"');"
            cursor.execute(sqlsave)
            conexion.commit()
            messagebox.showinfo("Datos Guardados", "Datos Guardados en la base de datos")
        else:
            messagebox.showinfo("Datos Guardados", "Error al conectar a la base de datos")
    else:
        messagebox.showinfo("Error de Guardado", "No se puede guardar datos vacios")

#botones de calculo y salida
boton = tkinter.Button(ventana, text="Calcular", command = suma, fg="blue")
boton.pack()
boton.place(x=30, y=200, height=15, width =50)
boton2 = tkinter.Button(ventana, text="Limpiar", command = limpiar, fg="grey")
boton2.pack()
boton2.place(x=100, y=200, height=15, width =50)
boton3 = tkinter.Button(ventana, text="Salir", command = salir, fg="red")
boton3.pack()
boton3.place(x=170, y=200, height=15, width =50)
boton4 = tkinter.Button(ventana, text="Guardar", command = guardar, fg="green")
boton4.pack()
boton4.place(x=240, y=200, height=15, width =50)
ventana.mainloop()
