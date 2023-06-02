import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import pydicom
import cv2
from PIL import Image,ImageTk,ImageGrab
from matplotlib import pyplot as plt

def implantes():
    def start_drag(event):
        global drag_data
        item = canvas.find_closest(event.x, event.y)[0]
        if item == canvas_image:
            drag_data["item"] = item
            drag_data["x"] = event.x
            drag_data["y"] = event.y
    def drag(event):
        global drag_data
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        canvas.move(drag_data["item"], dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y
    def end_drag(event):
        global drag_data
        drag_data["item"] = None
        drag_data["x"] = 0
        drag_data["y"] = 0
    def seleccionImplantes(valor):
        global im2, canvas_image,photo_image
        if valor=='DHS':
            print(valor)
            im2 = Image.open("./Imagenes/dhs.png").convert("RGBA")
            im2 = im2.resize((78, 171), Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(im2)
            canvas_image = canvas.create_image(50, 50, image=photo_image, anchor="nw")
            canvas.tag_bind(canvas_image, "<ButtonPress-1>", start_drag)
            canvas.tag_bind(canvas_image, "<B1-Motion>", drag)
            canvas.tag_bind(canvas_image, "<ButtonRelease-1>", end_drag)
            Ventana_implantes.destroy()
        else:
            im2 = Image.open('./Imagenes/clavo.jpg')
            im2.thumbnail((50,100))
            im2=ImageTk.PhotoImage(im2)
            label = ttk.Label(canvas, image=im2)
            label.place(x=50, y=50)
            canvas.tag_bind(canvas_image, "<ButtonPress-1>", start_drag)
            canvas.tag_bind(canvas_image, "<B1-Motion>", drag)
            canvas.tag_bind(canvas_image, "<ButtonRelease-1>", end_drag)



    Ventana_implantes = tk.Toplevel(root)
    Ventana_implantes.title("Implantes")
    Ventana_implantes.geometry("400x300")
    Ventana_implantes.iconbitmap('./hueso.ico')
    ttk.Label(Ventana_implantes, image=implantes_tk).place(x = 0, y = 0, relheight = 1, relwidth = 1)
    botonDHS=ttk.Button(Ventana_implantes,text='DHS',command=lambda:seleccionImplantes(botonDHS.cget('text')))
    botonDHS.place(x=200, y=70)
    botonClavo=ttk.Button(Ventana_implantes,text='Clavo',command=lambda:seleccionImplantes(botonClavo.cget('text')))
    botonClavo.place(x=200,y=200)
    
    
# Crea una ventana de Tkinter
drag_data = {"x": 0, "y": 0, "item": None}
canvas_image=''
root = tk.Tk()
# Carga la imagen
imagen = Image.open("./Imagenes/ana pau.png")
implantes_img = Image.open("./Fondos/Implantes.png")
implantes_tk = ImageTk.PhotoImage(implantes_img)
# Crea un canvas para mostrar la imagen
canvas = tk.Canvas(root, width=imagen.width, height=imagen.height)
canvas.pack()

# Crea una instancia de ImageTk para mostrar la imagen en Tkinter
imagen_tk = ImageTk.PhotoImage(imagen)

# Muestra la imagen en el canvas
fondoRx=canvas.create_image(0, 0, anchor=tk.NW, image=imagen_tk)

# Crea un botón debajo de la imagen
boton_implantes = tk.Button(root, text="Implantes", command=implantes)
boton_implantes.pack()

# Ejecuta el bucle principal de Tkinter
root.mainloop()
