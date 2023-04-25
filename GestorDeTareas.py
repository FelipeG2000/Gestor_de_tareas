import Funciones


def main():
    """inicializamos la funcion main donde se crean los diccionarios tareas y tareas_completadas
    """
    tareas = []
    tareas_completadas = []
    #llamamos la funcion menu ingresando los dos argumentos 
    Funciones.menu(tareas,tareas_completadas)    
    
if __name__=='__main__':
    main()  