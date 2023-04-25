import tkinter as tk
from datetime import datetime
import tkinter.messagebox as messagebox

def agregar_tarea(tareas):
    """Código para agregar tarea

    Args:
        tareas (_diccionario_): _Diccionario de tareas_
    """
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar tarea")

    etiqueta_nombre = tk.Label(ventana_agregar, text="Nombre:")
    etiqueta_nombre.pack(pady=5)

    entrada_nombre = tk.Entry(ventana_agregar, width=30)
    entrada_nombre.pack(pady=5)

    etiqueta_fecha_vencimiento = tk.Label(ventana_agregar, text="Fecha de vencimiento (YYYY-MM-DD):")
    etiqueta_fecha_vencimiento.pack(pady=5)

    entrada_fecha_vencimiento = tk.Entry(ventana_agregar, width=30)
    entrada_fecha_vencimiento.pack(pady=5)

    def agregar():
        #logica del boton "Agregar"
        nombre = entrada_nombre.get()
        fecha_vencimiento_str = entrada_fecha_vencimiento.get()
        #Agregando un par de filtros a la fecha de vencimiento 
        try:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "La fecha de vencimiento ingresada no es válida. Por favor ingrese una fecha en formato YYYY-MM-DD.")
            ventana_agregar.destroy()
            return
        fecha_ingreso = datetime.now().strftime("%Y-%m-%d")
        if fecha_vencimiento < datetime.now():
            messagebox.showerror("Error", "La fecha de vencimiento ingresada ya caduco. Por favor ingrese una fecha posterior al dia de hoy.")
            ventana_agregar.destroy()
            return
        tarea = {"nombre": nombre, "fecha_ingreso": fecha_ingreso, "fecha_vencimiento": fecha_vencimiento_str,}
        tareas.append(tarea)
        ventana_agregar.destroy()

    boton_agregar = tk.Button(ventana_agregar, text="Agregar", command=agregar)
    boton_agregar.pack(pady=10)

    boton_cancelar = tk.Button(ventana_agregar, text="Cancelar", command=ventana_agregar.destroy)
    boton_cancelar.pack(pady=5)
    

def mostrar_tareas(tareas,tareas_completadas):
    """Código para mostrar tareas

    Args:
        tareas (_lista_): _Diccionario de tareas_
        tareas_completadas (_type_): _Diccionario de tareas completadas_
    """
    ventana_mostrar = tk.Toplevel()
    ventana_mostrar.title("Mostrar tareas")

    etiqueta_tareas = tk.Label(ventana_mostrar, text="Tareas:")
    etiqueta_tareas.pack(pady=5)

    texto_tareas = tk.Text(ventana_mostrar, width=50, height=10)
    texto_tareas.pack(pady=5)

    texto_tareas.insert(tk.END, "Tareas por hacer:\n\n")
    #Mostramos las tareas en pantalla, si no hay mostramos que no hay 
    if not tareas:
        texto_tareas.insert(tk.END, "No tienes tareas por hacer\n\n")
    else:
        for tarea in tareas:
            nombre = tarea["nombre"]
            fecha_ingreso = tarea["fecha_ingreso"]
            fecha_vencimiento = tarea["fecha_vencimiento"]

            texto_tareas.insert(tk.END, f"Nombre: {nombre}\n")
            texto_tareas.insert(tk.END, f"Fecha de ingreso: {fecha_ingreso}\n")
            texto_tareas.insert(tk.END, f"Fecha de vencimiento: {fecha_vencimiento}\n\n")
            
    texto_tareas.insert(tk.END, "Tareas completadas:\n\n")
    #Mostramos las tareas completadas en panatalla, si no hay mostramos que no hay 
    if not tareas_completadas:
        texto_tareas.insert(tk.END, "No has completado ninguna tarea aun.")
    else:
        for tarea in tareas_completadas:
            nombre = tarea["nombre"]
            fecha_ingreso = tarea["fecha_ingreso"]
            fecha_vencimiento = tarea["fecha_vencimiento"]
            texto_tareas.insert(tk.END, f"Nombre: {nombre}\n")
            texto_tareas.insert(tk.END, f"Fecha de ingreso: {fecha_ingreso}\n")
            texto_tareas.insert(tk.END, f"Fecha de vencimiento: {fecha_vencimiento}\n\n")
    #Desactivamos la opcion de modifica el texto 
    texto_tareas.configure(state="disabled")

    boton_cerrar = tk.Button(ventana_mostrar, text="Cerrar", command=ventana_mostrar.destroy)
    boton_cerrar.pack(pady=10)
    
def completar_tarea(tareas,tareas_completadas):
    """Código para completar una tarea

    Args:
        tareas (_lista_): _Diccionario de tareas_
        tareas_completadas (_lista_): _Diccionario de tareas completadas_
    """
    ventana_completar = tk.Toplevel()
    ventana_completar.title("Completar tarea")

    etiqueta_tareas = tk.Label(ventana_completar, text="Tareas:")
    etiqueta_tareas.pack(pady=5)

    lista_tareas = tk.Listbox(ventana_completar, width=50, height=10)
    lista_tareas.pack(pady=5)
    #Mostramos en pantalla las tareas pendientes en una lista de seleccion 
    for tarea in tareas:
        nombre = tarea["nombre"]
        fecha_vencimiento = tarea["fecha_vencimiento"]
        lista_tareas.insert(tk.END, f"{nombre} ({fecha_vencimiento})")

    def completar():
        #Logica del boton "completar"
        seleccion = lista_tareas.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor seleccione una tarea.")
            ventana_completar.destroy()
            return
        tarea_completada = tareas[seleccion[0]]
        tareas_completadas.append(tarea_completada)
        tareas.remove(tarea_completada)
        
        messagebox.showinfo("Completada", f"La tarea {tarea_completada['nombre']} ha sido completada.")
        ventana_completar.destroy()

    boton_completar = tk.Button(ventana_completar, text="Completar tarea", command=completar)
    boton_completar.pack(pady=10)

    boton_cancelar = tk.Button(ventana_completar, text="Cancelar", command=ventana_completar.destroy)
    boton_cancelar.pack(pady=5)
    
def modificar_tarea(tareas):
    """Función para modificar tareas

    Args:
        tareas (_lista_): _diccionario de tareas_
    """
    def guardar_cambios():
        # Función para guardar los cambios en la tarea seleccionada
        nonlocal entrada_nombre, entrada_fecha_vencimiento, tareas, lista_tareas

        seleccion = lista_tareas.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor seleccione una tarea.")
            ventana_modificar.destroy()
            return
        tarea_seleccionada = tareas[seleccion[0]]

        # Se obtienen los valores de los campos de entrada de la ventana
        nombre = entrada_nombre.get()
        fecha_vencimiento_str = entrada_fecha_vencimiento.get()
        try:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "La fecha de vencimiento ingresada no es válida. Por favor ingrese una fecha en formato YYYY-MM-DD.")
            ventana_modificar.destroy()
            return
        if fecha_vencimiento < datetime.now():
            messagebox.showerror("Error", "La fecha de vencimiento ingresada ya caduco. Por favor ingrese una fecha posterior al dia de hoy.")
            ventana_modificar.destroy()
            return

        # Se actualiza la tarea
        tarea_seleccionada["nombre"] = nombre
        tarea_seleccionada["fecha_vencimiento"] = fecha_vencimiento.strftime("%Y-%m-%d")


        # Se cierra la ventana
        ventana_modificar.destroy()

    # Código para crear ventana de modificar tarea
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar tarea")

    etiqueta_tareas = tk.Label(ventana_modificar, text="Tareas:")
    etiqueta_tareas.pack(pady=5)

    lista_tareas = tk.Listbox(ventana_modificar, width=50, height=10)
    lista_tareas.pack(pady=5)

    #Entrada del nuevo nombre
    etiqueta_nombre = tk.Label(ventana_modificar, text="Nombre")
    etiqueta_nombre.pack(pady=1)
    entrada_nombre = tk.Entry(ventana_modificar, width=30)
    entrada_nombre.pack(pady=5)
    entrada_nombre.insert(0, "")

    #Entrada de la nueva fecha de vencimiento
    etiqueta_fecha = tk.Label(ventana_modificar, text="Fecha de vencimiento")
    etiqueta_fecha.pack(pady=1)
    entrada_fecha_vencimiento = tk.Entry(ventana_modificar, width=30)
    entrada_fecha_vencimiento.pack(pady=5)
    entrada_fecha_vencimiento.insert(0, "")

    #pintamos las tareas
    for tarea in tareas:
        nombre = tarea["nombre"]
        fecha_vencimiento = tarea["fecha_vencimiento"]
        lista_tareas.insert(tk.END, f"{nombre} ({fecha_vencimiento})")

    boton_guardar = tk.Button(ventana_modificar, text="Guardar cambios", command=guardar_cambios)
    boton_guardar.pack(pady=10)

    # Se obtiene la tarea seleccionada y se muestran sus valores en campos de entrada
    seleccion = lista_tareas.curselection()
    if seleccion:
        tarea_seleccionada = tareas[seleccion[0]]
        nombre_anterior = tarea_seleccionada["nombre"]
        fecha_vencimiento_anterior = tarea_seleccionada["fecha_vencimiento"]

        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, nombre_anterior)

        entrada_fecha_vencimiento.delete(0, tk.END)
        entrada_fecha_vencimiento.insert(0, fecha_vencimiento_anterior)
    


def menu(tareas,tareas_completadas):
    """Menu pricipal, aca estaran los botones y la esencia del programa

    Args:
        tareas (_lista_): _Diccionario de tareas_
        tareas_completadas (_lista_): _Diccionario de tareas completadas_
    """
     #los argumentos tareas y tareas_completadas son los que le estaremos pasando a las funciones
     
     #Creamos la ventana con los botones, estos tienen funciones "lambda" por que el comando "command" no recive funciones con parametros
    ventana = tk.Tk()
    ventana.title("Gestor de Tareas")

    etiqueta = tk.Label(ventana, text="Selecciona una opción:",width=50)
    etiqueta.pack(pady=10)

    boton_agregar = tk.Button(ventana, text="Agregar tarea", command=lambda:agregar_tarea(tareas))
    boton_agregar.pack(pady=5)

    boton_mostrar = tk.Button(ventana, text="Mostrar tareas", command=lambda:mostrar_tareas(tareas,tareas_completadas))
    boton_mostrar.pack(pady=5)

    boton_modificar = tk.Button(ventana, text="Modificar tarea", command=lambda:modificar_tarea(tareas))
    boton_modificar.pack(pady=5)

    boton_completar = tk.Button(ventana, text="Completar tarea", command=lambda:completar_tarea(tareas,tareas_completadas))
    boton_completar.pack(pady=5)

    boton_salir = tk.Button(ventana, text="Salir", command=ventana.quit)
    boton_salir.pack(pady=10)
    
    ventana.mainloop()