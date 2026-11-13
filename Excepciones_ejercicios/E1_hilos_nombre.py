import threading
import time

#funcion que recibe el nombre y el numero de saludos por persona
def saludar(nombre, saludos):
    try:
        for i in range(saludos):
            print(f"{nombre}: hola {i}")
            time.sleep(1)
    except TypeError:
        print(f"Los saludos deben ser un numero entero")
    

def main():
    personas = [("Ana", 3), ("Beto", 5), ("Cora", 2)]
    #crear el arrglo de hilos para posteriormente terminarlos uno a uno
    hilos = []

    #por cada persona crear un hilo de ejecucion 
    """ se tiene como target a la funcioon saludar que es la encargada
        de mostrar los saludos en salida estandar """
    for nombre, cantidad in personas:
        hilo = threading.Thread(target=saludar, args=(nombre,cantidad))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()
        
    print("Fin del programa")

main()


