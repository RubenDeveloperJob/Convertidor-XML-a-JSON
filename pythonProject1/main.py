# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter as tk
from tkinter import filedialog, scrolledtext
import xml.etree.ElementTree as ET
import json
import os
import xmlschema
import webbrowser


def validar_xml():
    global ruta_xml

    ruta_xml = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if not ruta_xml:
        return

    try:
        xml_schema = xmlschema.XMLSchema('esquema.xsd')  # Reemplaza 'esquema.xsd' con tu propio esquema
        xml_schema.validate(ruta_xml)
        resultado.config(text="El XML es válido.", fg="green")
        boton_abrir_navegador.config(state="disabled")  # Deshabilitar el botón para abrir en navegador
    except Exception as e:
        resultado.config(text="Error de validación XML: " + str(e), fg="red")


def mostrar_xml():
    try:
        ventana_xml = tk.Toplevel()
        ventana_xml.title("Contenido del XML")

        with open(ruta_xml, 'r') as archivo_xml:
            contenido = archivo_xml.read()

        texto_xml = scrolledtext.ScrolledText(ventana_xml, width=60, height=20)
        texto_xml.insert(tk.END, contenido)
        texto_xml.pack()
    except Exception as e:
        resultado.config(text="Error al mostrar el XML: " + str(e), fg="red")


def mostrar_json():
    try:
        if not os.path.exists(ruta_json):
            resultado.config(text="No se encontró el archivo JSON.", fg="red")
            return

        ventana_json = tk.Toplevel()
        ventana_json.title("Contenido del JSON")

        with open(ruta_json, 'r') as archivo_json:
            contenido = archivo_json.read()

        texto_json = scrolledtext.ScrolledText(ventana_json, width=60, height=20)
        texto_json.insert(tk.END, contenido)
        texto_json.pack()
    except Exception as e:
        resultado.config(text="Error al mostrar el JSON: " + str(e), fg="red")


def guardar_json():
    try:
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".json")
        if not ruta_guardado:
            return

        with open(ruta_json, 'r') as archivo_json:
            contenido = archivo_json.read()

        with open(ruta_guardado, 'w') as archivo_guardado:
            archivo_guardado.write(contenido)

        resultado.config(text="El archivo JSON ha sido guardado como " + ruta_guardado, fg="green")
    except Exception as e:
        resultado.config(text="Error al guardar el JSON: " + str(e), fg="red")


def abrir_en_navegador():
    try:
        webbrowser.open('file://' + os.path.abspath(ruta_json), new=2)
    except Exception as e:
        resultado.config(text="Error al abrir en el navegador: " + str(e), fg="red")


def convertir_xml_a_json():
    global ruta_json

    try:
        tree = ET.parse(ruta_xml)
        root = tree.getroot()

        datos_json = []

        for child in root:
            libro = {}
            for element in child:
                libro[element.tag] = element.text
            datos_json.append(libro)

        ruta_json = os.path.splitext(ruta_xml)[0] + ".json"

        with open(ruta_json, 'w') as archivo_json:
            json.dump(datos_json, archivo_json, indent=4)

        resultado.config(text="¡Conversión exitosa! El archivo JSON ha sido guardado como " + ruta_json, fg="green")
        boton_abrir_navegador.config(state="normal")  # Habilitar el botón para abrir en navegador
    except Exception as e:
        resultado.config(text="Error durante la conversión a JSON: " + str(e), fg="red")


# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Convertir XML a JSON")
ventana.geometry("600x300")  # Tamaño de la ventana

# Colores
color_fondo = "#F0F0F0"
color_botones = "#4CAF50"  # Verde
color_bordes = "#CCCCCC"

# Crear marco para los controles principales
marco_controles = tk.Frame(ventana, bg=color_fondo)
marco_controles.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# Botones y etiquetas
boton_validar_xml = tk.Button(marco_controles, text="Validar XML", command=validar_xml, bg=color_botones)
boton_validar_xml.grid(row=0, column=0, padx=10, pady=10)

boton_seleccionar_xml = tk.Button(marco_controles, text="Seleccionar XML", command=convertir_xml_a_json,
                                  bg=color_botones)
boton_seleccionar_xml.grid(row=1, column=0, padx=10, pady=10)

boton_mostrar_xml = tk.Button(marco_controles, text="Mostrar XML", command=mostrar_xml, bg=color_botones)
boton_mostrar_xml.grid(row=2, column=0, padx=10, pady=10)

boton_mostrar_json = tk.Button(marco_controles, text="Mostrar JSON", command=mostrar_json, bg=color_botones)
boton_mostrar_json.grid(row=3, column=0, padx=10, pady=10)

boton_guardar_json = tk.Button(marco_controles, text="Guardar JSON", command=guardar_json, bg=color_botones)
boton_guardar_json.grid(row=4, column=0, padx=10, pady=10)

boton_abrir_navegador = tk.Button(marco_controles, text="Abrir en Navegador", command=abrir_en_navegador,
                                  bg=color_botones, state="disabled")
boton_abrir_navegador.grid(row=5, column=0, padx=10, pady=10)

resultado = tk.Label(marco_controles, text="", bg=color_fondo)
resultado.grid(row=6, column=0, padx=10, pady=10)

ventana.mainloop()



