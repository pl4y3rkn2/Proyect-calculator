from email import message
from pickle import READONLY_BUFFER
from sqlite3 import Cursor, connect
import tkinter as tk
from tkinter import LEFT, Label, Tk, ttk
import tkinter
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from bokeh.plotting import figure, output_file, show


#Opciones de la window
hour = datetime.now()
window = tk.Tk() #windows on object
window.title("Calcutest, "+hour.strftime("%H:%M:%S")) #name's window
window.config(width=300, height=250, bg="grey") #width, height and background

#Text's box y label
label1 = Label(window, text="Bill 1") #Label
label1.pack(side=LEFT)
label1.place(x=20, y=20)
label1.config(bg="grey")

entry1 = ttk.Entry(justify=tk.LEFT, width=10) #Text's box
entry1.place(x=65, y=20)

label2 = Label(window, text="Bill 2") #Label
label2.pack(side=LEFT)
label2.place(x=20, y=40)
label2.config(bg="grey")

entry2 = ttk.Entry(justify=tk.LEFT, width=10) #Text's box
entry2.place(x=65, y=40)

label3 = Label(window, text="Bill 3") #Label
label3.pack(side=LEFT)
label3.place(x=20, y=60)
label3.config(bg="grey")

entry3 = ttk.Entry(justify=tk.LEFT, width=10) #Text's box
entry3.place(x=65, y=60)

label4 = Label(window, text="Gold value/$") #Label
label4.pack(side=LEFT)
label4.place(x=139, y=20)
label4.config(bg="grey")

entry4 = ttk.Entry(justify=tk.LEFT, width=10) #Text's box
entry4.place(x=211, y=20)

subtotal = ttk.Entry(justify=tk.LEFT, width=12, takefocus=False, state="normal") #Text's box
subtotal.place(x=20, y=100)

labelsubtotal = Label(window, text="Total accumulated gold") #Label
labelsubtotal.pack(side=LEFT)
labelsubtotal.place(x=100, y=100)
labelsubtotal.config(bg="grey")

total = ttk.Entry(justify=tk.LEFT, width=12, takefocus=False, state="normal") #Text's box
total.place(x=20, y=120)

labeltotal = Label(window, text="Total gold minus 5%") #Label
labeltotal.pack(side=LEFT)
labeltotal.place(x=100, y=120)
labeltotal.config(bg="grey")

dollarforgold = ttk.Entry(justify=tk.LEFT, width=12, takefocus=False, state="normal") #Text's box
dollarforgold.place(x=20, y=140)

labeldollarforgold = Label(window, text="$/gold") #Label
labeldollarforgold.pack(side=LEFT)
labeldollarforgold.place(x=100, y=140)
labeldollarforgold.config(bg="grey")

# Save Function
try:
    with open("oro.txt", "r", encoding="utf-8") as f:
        entry1.insert(0, int(f.readline()))
        entry2.insert(0, int(f.readline()))
        entry3.insert(0, int(f.readline()))
        entry4.insert(0, float(f.readline()))
        subtotal.insert(0, int(f.readline()))
        total.insert(0, float(f.readline()))
        dollarforgold.insert(0, float(f.readline()))    
        f.close()
except ValueError:
    entry1.insert(0, int(0))
    entry2.insert(0, int(0))
    entry3.insert(0, int(0))
    entry4.insert(0, float(0))
    subtotal.insert(0, int(0))
    total.insert(0, float(0))
    dollarforgold.insert(0, float(0))
# button function

def sum():
    try:
        sum1 = int(entry1.get())
        sum2 = int(entry2.get())
        sum3 = int(entry3.get())
        price = float(entry4.get())
        totalsum = sum1+sum2+sum3
        subtotal.delete(0,tk.END)
        total.delete(0,tk.END)
        dollarforgold.delete(0,tk.END)
        subtotal.insert(0, totalsum)
        total.insert(0, round(totalsum*0.95,2))
        totalsum *= 0.95
        dollarforgold.insert(0, round(totalsum/1000*price,2))
    except ValueError:
        messagebox.showinfo("Calculation Error", "can only calculate integers")
        

def clear():
    question=messagebox.askquestion("Clear","Would you like to Erase all data?")
    if question=="yes":
        entry1.delete(0,tk.END)
        entry2.delete(0,tk.END)
        entry3.delete(0,tk.END)
        entry4.delete(0,tk.END)
        subtotal.delete(0,tk.END)
        total.delete(0,tk.END)
        dollarforgold.delete(0,tk.END)
        entry1.insert(0, int(0))
        entry2.insert(0, int(0))
        entry3.insert(0, int(0))
        entry4.insert(0, int(0))
        subtotal.insert(0, int(0))
        total.insert(0, int(0))
        dollarforgold.insert(0, float(0))

def exit():
    question=messagebox.askquestion("Quit","Do you want to close the application?")
    if question=="yes":
        window.destroy()
    
def save():
    if subtotal.get()!="0":

        #Save local application data
        with open("oro.txt", "w") as f:
            f.write(entry1.get()+"\n")
            f.write(entry2.get()+"\n")
            f.write(entry3.get()+"\n")
            f.write(entry4.get()+"\n")
            f.write(subtotal.get()+"\n")
            f.write(total.get()+"\n")
            f.write(dollarforgold.get()+"\n")
            f.close()

            #connection to the database, data storage and others
            try:
                conexion = mysql.connector.connect(user="root", password="", host="localhost", database="db", port="3306")
                print(conexion)
                cursor = conexion.cursor()
                sqlsave = "INSERT INTO `datos` (`cuenta1`, `cuenta2`, `cuenta3`, `DG`, `total`, `fecha`) VALUES ('"+entry1.get()+"', '"+entry2.get()+"', '"+entry3.get()+"', '"+entry4.get()+"', '"+subtotal.get()+"', '"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"');"
                cursor.execute(sqlsave)
                conexion.commit()
                messagebox.showinfo("Saved Data", "Data Saved in the database\n", conexion)
            except mysql.connector.errors.InterfaceError:
                messagebox.showinfo("Data Saved", "Error connecting to database")
    else:
        messagebox.showinfo("Save Error", "Cannot save empty data")

def graphic():
    conexion = mysql.connector.connect(user="root", password="", host="localhost", database="db", port="3306")
    cursor = conexion.cursor()

    cursor.execute("SELECT `cuenta1` FROM `datos`")
    vals1 = cursor.fetchall()
    cursor.execute("SELECT `cuenta2` FROM `datos`")
    vals2 = cursor.fetchall()
    cursor.execute("SELECT `cuenta3` FROM `datos`")
    vals3 = cursor.fetchall()
    cursor.execute("SELECT `DG` FROM `datos`")
    vals4 = cursor.fetchall()
    cursor.execute("SELECT `total` FROM `datos`")
    vals5 = cursor.fetchall()
    cursor.execute("SELECT `fecha` FROM `datos`")
    vals6 = cursor.fetchall()
    conexion.close()

    output_file('simple_save.html')
    fig = figure(title="Gold's Data", x_axis_label="x", y_axis_label="y")
        
    fig.line(x=vals6, y=vals1, legend_label="Bill 1", color="Blue", line_width=2)
    fig.line(x=vals6, y=vals2, legend_label="Bill 2", color="red", line_width=2)
    fig.line(x=vals6, y=vals3, legend_label="Bill 3", color="green", line_width=2)
    fig.line(x=vals6, y=vals4, legend_label="$/G", color="black", line_width=1)
    fig.line(x=vals6, y=vals5, legend_label="Total", color="grey", line_width=2)
    show(fig)
        
#calculate and exit buttons
boton = tkinter.Button(window, text="Calculate", command = sum, fg="blue")
boton.pack()
boton.place(x=30, y=200, height=15, width =50)
boton2 = tkinter.Button(window, text="Clear", command = clear, fg="grey")
boton2.pack()
boton2.place(x=100, y=200, height=15, width =50)
boton3 = tkinter.Button(window, text="Exit", command = exit, fg="red")
boton3.pack()
boton3.place(x=170, y=200, height=15, width =50)
boton4 = tkinter.Button(window, text="Save", command = save, fg="green")
boton4.pack()
boton4.place(x=240, y=200, height=15, width =50)
boton5 = tkinter.Button(window, text="Graphic", command = graphic, fg="blue")
boton5.pack()
boton5.place(x=30, y=220, height=15, width =50)
window.mainloop()
